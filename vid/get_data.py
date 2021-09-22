import requests
import pandas as pd

from datetime import datetime
import time
import io
import json

from django.utils.timezone import make_aware
from django.db.utils import IntegrityError
from django.core.cache import cache

from vid.models import (PennCases,
                        PennDeaths,
                        PennHospitals,
                        CasesDeathsNTY,
                        MetricsActNow,
                        AllNTY)
from covid_tracker.settings import APP_URL

api_key = '776e4ec57ee346d6a0a2a4abb6b006a8'
act_now_api = f'https://api.covidactnow.org/v2/counties.timeseries.json?apiKey={api_key}'

oklahoma_files = 'https://storage.googleapis.com/' \
                 'ok-covid-gcs-public-download/oklahoma_cases_county.csv'

nyt_timeseries = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv'
nyt_live = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/live/us-counties.csv'
nyt_all = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv'

focus_fips = {'42101': 'philly',
              '42111': 'somerset',
              '53033': 'king',
              # '17043': 'dupage',
              '17089': 'kane',
              '40027': 'cleveland',
              '40109': 'oklahoma',
              '06037': 'los angeles'}


def refresh_penn_cases():
    PennCases.objects.all().delete()


def refresh_penn_deaths():
    PennDeaths.objects.all().delete()


def refresh_penn_hospital():
    PennHospitals.objects.all().delete()


# noinspection DuplicatedCode
def load_nyt(include_live=False):
    """
    load case/death time series from nyt github csv.

    Free heroku dyno has buffer limit of 1mb so request is broken into chunks
    free heroku postgres db has limit of only 10k rows, so
        only includes the locations in focus_fips.
    """
    CasesDeathsNTY.objects.all().delete()

    r = requests.get(nyt_timeseries, stream=True)
    size = 0
    content = io.BytesIO()
    num_chunks = 0

    for chunk in r.iter_content(750000):
        size += len(chunk)
        content.write(chunk)
        num_chunks += 1
    content.seek(0)

    print('received nyt data')

    # nyt_data = requests.get(nyt_timeseries).content
    nyt_data = pd.read_csv(content,
                           encoding='utf8',
                           sep=",",
                           parse_dates=['date'],
                           dtype={'fips': str})
    nyt_data = nyt_data.where(pd.notnull(nyt_data), None)

    # keep only the FIPS that i care about
    nyt_data = nyt_data[nyt_data['fips'].isin(list(focus_fips.keys()))]

    print('read nyt data')

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
            nyt_cases.append(CasesDeathsNTY(date=aware_date,
                                            county=row['county'],
                                            state=row['state'],
                                            fips=row['fips'],
                                            cases=row['cases'],
                                            deaths=row['deaths'],
                                            ))

        print(f'created nyt objects in pd ending at index {end_index} of {len(nyt_data)}')

        try:
            CasesDeathsNTY.objects.bulk_create(nyt_cases)
            print('nyt data successfully imported')
        except IntegrityError:
            print('nyt data failed to import')

    if include_live:
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
            nyt_cases_live.append(CasesDeathsNTY(date=aware_date,
                                                 county=row['county'],
                                                 state=row['state'],
                                                 fips=row['fips'],
                                                 cases=row['cases'],
                                                 deaths=row['deaths'],
                                                 ))

        try:
            CasesDeathsNTY.objects.bulk_create(nyt_cases_live)
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
    AllNTY.objects.all().delete()

    r = requests.get(nyt_all, stream=True)
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
            nyt_cases.append(CasesDeathsNTY(date=aware_date,
                                            cases=row['cases'],
                                            deaths=row['deaths'],
                                            ))

        print(f'created nyt objects in pd ending at index {end_index} of {len(nyt_data)}')

        try:
            AllNTY.objects.bulk_create(nyt_cases)
            print('all US nyt data successfully imported')
        except IntegrityError:
            print('all US nyt data failed to import')


def load_actnow(fips):
    api_single = f'https://api.covidactnow.org/v2/county/{fips}.timeseries.json?apiKey={api_key}'
    raw = requests.get(api_single).content
    raw_dict = json.loads(raw.decode('utf-8'))

    fips_pulled = raw_dict['fips']

    population = raw_dict['population']
    state = raw_dict['state']
    county = raw_dict['county']

    metrics = pd.DataFrame(raw_dict['metricsTimeseries'])

    act_now_objects = []
    for index, row in metrics.iterrows():
        dumb_date = datetime.strptime(row['date'], "%Y-%m-%d")
        aware_date = make_aware(dumb_date)
        act_now_objects.append(MetricsActNow(date=aware_date,
                                             state=state,
                                             county=county,
                                             fips=fips_pulled,
                                             population=population,
                                             testPositivityRatio=row['testPositivityRatio'],
                                             infectionRate=row['infectionRate']
                                             ))

    try:
        MetricsActNow.objects.bulk_create(act_now_objects)
        print(f'CovidActNow data for {county} successfully imported')
    except IntegrityError:
        print(f'CovidActNow data for {county} failed to import')


def load_all_actnow():
    MetricsActNow.objects.all().delete()

    for fips in focus_fips:
        load_actnow(fips=fips)


def cache_pages(running_local=False):
    # clear existing cache
    cache.clear()

    pages = ['somerset',
             'philly',
             'king',
             'kane',
             'oklahoma',
             # 'dupage',
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
