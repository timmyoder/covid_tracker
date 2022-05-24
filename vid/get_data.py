import requests
import datetime as dt

import pandas as pd

import io
import json

from django.utils.timezone import make_aware
from django.db.utils import IntegrityError
from django.core.cache import cache

from vid.models import CountyMetrics, EntireUS
from covid_tracker.settings import APP_URL

api_key = '776e4ec57ee346d6a0a2a4abb6b006a8'
act_now_api = f'https://api.covidactnow.org/v2/counties.timeseries.json?apiKey={api_key}'

nyt_timeseries = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv'
nyt_live = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/live/us-counties.csv'
nyt_all = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv'

CURRENT_YEAR = dt.datetime.now().year
PREVIOUS_YEARS = [year for year in range(2020, CURRENT_YEAR)]

focus_fips = {'42101': 'philly',
              '42111': 'somerset',
              '53033': 'king',
              '17043': 'dupage',
              '17089': 'kane',
              '40027': 'cleveland',
              '40109': 'oklahoma',
              '06037': 'los angeles'}


def get_nyt_file_name(year):
    return f'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties-{year}.csv'


def retrieve_nyt(year):
    print('retrieving nyt data')
    url = get_nyt_file_name(year)
    r = requests.get(url, stream=True, timeout=5)
    size = 0
    content = io.BytesIO()
    num_chunks = 0

    for chunk in r.iter_content(750000):
        size += len(chunk)
        content.write(chunk)
        num_chunks += 1
    content.seek(0)

    print('received nyt data')

    nyt_data = pd.read_csv(content,
                           encoding='utf8',
                           sep=",",
                           parse_dates=['date'],
                           dtype={'fips': str})
    nyt_data = nyt_data.where(pd.notnull(nyt_data), None)

    # keep only the FIPS that i care about
    nyt_data = nyt_data[nyt_data['fips'].isin(list(focus_fips.keys()))]
    nyt_data['date'] = pd.to_datetime(nyt_data['date'], format="%Y-%m-%d", utc=True)

    print('read nyt data')

    return nyt_data, num_chunks


def retrieve_single_actnow(fips, year=CURRENT_YEAR):
    api_single = f'https://api.covidactnow.org/v2/county/{fips}.timeseries.json?apiKey={api_key}'
    raw = requests.get(api_single).content
    raw_dict = json.loads(raw.decode('utf-8'))

    population = raw_dict['population']

    metrics = pd.DataFrame(raw_dict['metricsTimeseries'])
    metrics['date'] = pd.to_datetime(metrics['date'], format="%Y-%m-%d", utc=True)
    metrics = metrics[['date', 'testPositivityRatio', 'infectionRate']]
    metrics['population'] = population
    metrics['fips'] = fips

    metrics['year'] = metrics['date'].dt.year
    metrics = metrics[metrics['year'] == year]

    print(f'CovidActNow data for {focus_fips[fips]} successfully downloaded')
    return metrics


def retrieve_all_actnow(year=CURRENT_YEAR):
    all_actnow_data = pd.DataFrame()
    for fips in focus_fips:
        single_county_data = retrieve_single_actnow(fips=fips, year=year)
        all_actnow_data = all_actnow_data.append(single_county_data, ignore_index=True)

    return all_actnow_data


# noinspection DuplicatedCode
def load_metrics(year=CURRENT_YEAR):
    """
    load case/death time series from nyt github csv.

    Free heroku dyno has buffer limit of 1mb so request is broken into chunks
    free heroku postgres db has limit of only 10k rows, so
        only includes the locations in focus_fips.
    """

    print(f'updating data for {year}')

    CountyMetrics.objects.filter(date__year=year).delete()

    print(f'models deleted for {year}')

    nyt_data, num_chunks = retrieve_nyt(year)

    actnow_metrics = retrieve_all_actnow(year)

    all_data = pd.merge(nyt_data, actnow_metrics, on=['date', 'fips'], how='left')

    chunk_size = round(len(all_data) / (num_chunks + 1))
    current_index = 0

    while current_index < len(all_data) - 1:
        end_index = current_index + chunk_size
        if end_index > len(all_data) - 1:
            chunks_dataframe = all_data.iloc[current_index:]
        else:
            chunks_dataframe = all_data[current_index:end_index]

        current_index += chunk_size

        metrics_objects = []
        for index, row in chunks_dataframe.iterrows():
            metrics_objects.append(CountyMetrics(date=row['date'],
                                                 county=row['county'],
                                                 state=row['state'],
                                                 fips=row['fips'],
                                                 cases=row['cases'],
                                                 deaths=row['deaths'],
                                                 population=row['population'],
                                                 testPositivityRatio=row['testPositivityRatio'],
                                                 infectionRate=row['infectionRate']
                                                 ))

        print(f'created metrics objects in pd ending at index {end_index} of {len(all_data)}')

        try:
            CountyMetrics.objects.bulk_create(metrics_objects)
            print(f'All metrics data successfully imported for {year}')
        except IntegrityError:
            print(f'Metrics data failed to import for {year}')


def load_live_nyt():
    nyt_live_data = requests.get(nyt_live).content
    nyt_live_data = pd.read_csv(io.BytesIO(nyt_live_data),
                                encoding='utf8',
                                sep=",",
                                parse_dates=['date'],
                                dtype={'fips': str})
    nyt_live_data = nyt_live_data.where(pd.notnull(nyt_live_data), None)
    nyt_live_data = nyt_live_data[nyt_live_data['fips'].isin(list(focus_fips.keys()))]

    nyt_cases_live = []

    for index, row in nyt_live_data.iterrows():
        aware_date = make_aware(row['date'])
        nyt_cases_live.append(CountyMetrics(date=aware_date,
                                            county=row['county'],
                                            state=row['state'],
                                            fips=row['fips'],
                                            cases=row['cases'],
                                            deaths=row['deaths'],
                                            ))

    try:
        CountyMetrics.objects.bulk_create(nyt_cases_live)
        print('nyt live data successfully imported')
    except IntegrityError:
        print('nyt live data failed to import')


def load_nyt_all_us():
    """
    load case/death time series from nyt github csv for the entire US.

    Free heroku dyno has buffer limit of 1mb so request is broken into chunks
    free heroku postgres db has limit of only 10k rows, so
        only includes the locations in focus_fips.
    """
    EntireUS.objects.all().delete()

    r = requests.get(nyt_all, stream=True, timeout=5)
    size = 0
    content = io.BytesIO()
    num_chunks = 0

    for chunk in r.iter_content(750000):
        size += len(chunk)
        content.write(chunk)
        num_chunks += 1
    content.seek(0)

    print('received all US nyt data')

    nyt_data = pd.read_csv(content,
                           encoding='utf8',
                           sep=",",
                           parse_dates=['date'])
    nyt_data = nyt_data.where(pd.notnull(nyt_data), None)

    print('read all US nyt data')

    chunk_size = round(len(nyt_data) / (num_chunks + 1))
    current_index = 0

    while current_index < len(nyt_data) - 1:
        end_index = current_index + chunk_size
        if end_index > len(nyt_data) - 1:
            chunks_dataframe = nyt_data.iloc[current_index:]
        else:
            chunks_dataframe = nyt_data[current_index:end_index]

        current_index += chunk_size

        nyt_cases = []
        for index, row in chunks_dataframe.iterrows():
            aware_date = make_aware(row['date'])
            nyt_cases.append(CountyMetrics(date=aware_date,
                                           cases=row['cases'],
                                           deaths=row['deaths'],
                                           ))

        print(f'created nyt objects in pd ending at index {end_index} of {len(nyt_data)}')

        try:
            EntireUS.objects.bulk_create(nyt_cases)
            print('all US nyt data successfully imported')
        except IntegrityError:
            print('all US nyt data failed to import')


def cache_pages(running_local=False):
    # clear existing cache
    cache.clear()

    pages = ['somerset',
             'philly',
             'king',
             'kane',
             'oklahoma',
             'dupage',
             'cleveland',
             'la',
             'comparison'
             ]
    if not running_local:
        url = APP_URL
    else:
        url = 'http://127.0.0.1:8000/'

    # load all pages into the cache with fresh data
    for page in pages:
        req = requests.get(url=f'{url}{page}')
        content = req.content
        if 'Yoder' in content.decode():
            print(f'{page} page cached: {req.status_code}')
        else:
            print(f'{page} page caching failed')
