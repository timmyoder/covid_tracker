import requests
import pandas as pd

from datetime import datetime
import time
import io
import json

from django.utils.timezone import make_aware
from django.db.utils import IntegrityError
from django.core.cache import cache

from vid.models import (Places,
                        PennCases,
                        PennDeaths,
                        PennHospitals,
                        CasesDeathsNTY,
                        MetricsActNow,
                        AllNTY)
from covid_tracker.settings import APP_URL

api_key = '776e4ec57ee346d6a0a2a4abb6b006a8'
act_now_api = f'https://api.covidactnow.org/v2/counties.timeseries.json?apiKey={api_key}'

penn_cases = 'https://data.pa.gov/resource/j72v-r42c.json'
penn_deaths = 'https://data.pa.gov/resource/fbgu-sqgp.json'
penn_hospital = 'https://data.pa.gov/resource/kayn-sjhx.json'

oklahoma_files = 'https://storage.googleapis.com/' \
                 'ok-covid-gcs-public-download/oklahoma_cases_county.csv'

nyt_timeseries = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv'
nyt_live = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/live/us-counties.csv'
nyt_all = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv'

focus_fips = {'42101': 'philly',
              '42111': 'somerset',
              '53033': 'king',
              '17043': 'dupage',
              '17089': 'kane',
              '40027': 'cleveland',
              '40109': 'oklahoma',
              '06037': 'los angeles'}


def pull_penn_data(api, county):
    clean_df = pd.DataFrame(requests.get(f'{api}?county={county}').json())
    clean_df['date'] = pd.to_datetime(clean_df['date'])
    clean_df = clean_df.set_index('date').sort_index()
    clean_df.drop(columns=['county'], inplace=True)
    clean_df = clean_df.astype(float)
    return clean_df


def get_penn_data(county):
    """
    Retrieve data from Penn dept health for a specified county

    Returns a tuple of (case_data_df, death_data_df, hospital_data_df)
    """
    cases = pull_penn_data(penn_cases, county)
    deaths = pull_penn_data(penn_deaths, county)
    hospital = pull_penn_data(penn_hospital, county)

    return cases, deaths, hospital


def refresh_penn_cases():
    county_data = []
    for county in ['Somerset', 'Philadelphia']:
        cases = requests.get(f'{penn_cases}?county={county}').json()
        county_data.append(cases)

    t1 = time.perf_counter()

    # print(f'{t1 - tic} seconds download')

    PennCases.objects.all().delete()

    # t2 = time.perf_counter()
    # print(f'{t2 - t1} seconds delete')

    for cases in county_data:
        objects = []
        for case in cases:
            date = datetime.strptime(case.get('date'), "%Y-%m-%dT%H:%M:%S.%f")
            aware_date = make_aware(date)
            obj = PennCases(cases=float(case.get('cases')),
                            county=case.get('county'),
                            date=aware_date,
                            cases_avg_new=float(case.get('cases_avg_new', 0)),
                            cases_cume=int(case.get('cases_cume')),
                            population=int(float(case.get('population'))),
                            cases_rate=float(case.get('cases_rate')),
                            cases_avg_new_rate=float(case.get('cases_avg_new_rate', 0)),
                            cases_cume_rate=float(case.get('cases_cume_rate')),
                            )
            objects.append(obj)

        try:
            PennCases.objects.bulk_create(objects)
            # noinspection PyUnboundLocalVariable
            print(f'{case.get("county")} cases success')
        except IntegrityError:
            print(f'{case.get("county")} cases failure')


def refresh_penn_deaths():
    PennDeaths.objects.all().delete()

    county_data = []
    for county in ['Somerset', 'Philadelphia']:
        deaths = requests.get(f'{penn_deaths}?county={county}').json()
        county_data.append(deaths)

    for deaths in county_data:
        objects = []
        for death in deaths:
            date = datetime.strptime(death.get('date'), "%Y-%m-%dT%H:%M:%S.%f")
            aware_date = make_aware(date)
            obj = PennDeaths(deaths=float(death.get('deaths')),
                             county=death.get('county'),
                             date=aware_date,
                             deaths_cume=float(death.get('deaths_cume')),
                             population=float(death.get('population')),
                             deaths_rate=float(death.get('deaths_rate')),
                             deaths_cume_rate=float(death.get('deaths_cume_rate')),
                             )

            objects.append(obj)

        try:
            PennDeaths.objects.bulk_create(objects)
            # noinspection PyUnboundLocalVariable
            print(f'{death.get("county")} deaths success')
        except IntegrityError:
            print(f'{death.get("county")} deaths failure')


def refresh_penn_hospital():
    PennHospitals.objects.all().delete()

    # county_data = []
    # for county in ['Somerset', 'Philadelphia']:
    #     hospital_data = requests.get(f'{penn_hospital}?county={county}').json()
    #     county_data.append(hospital_data)
    #
    # for hospital_data in county_data:
    #     objects = []
    #     for entry in hospital_data:
    #         date = datetime.strptime(entry.get('date'), "%Y-%m-%dT%H:%M:%S.%f")
    #         aware_date = make_aware(date)
    #         obj = PennHospitals(county=entry.get('county'),
    #                             date=aware_date,
    #                             aii_avail=float(entry.get('aii_avail', 0)),
    #                             aii_total=float(entry.get('aii_total', 0)),
    #                             icu_avail=float(entry.get('icu_avail', 0)),
    #                             icu_total=float(entry.get('icu_total', 0)),
    #                             med_avail=float(entry.get('med_avail', 0)),
    #                             med_total=float(entry.get('med_total', 0)),
    #                             covid_patients=float(entry.get('covid_patients', 0)),
    #                             aii_percent=float(entry.get('aii_percent', 0)),
    #                             icu_percent=float(entry.get('icu_percent', 0)),
    #                             med_percent=float(entry.get('med_percent', 0))
    #                             )
    #
    #         objects.append(obj)
    #
    #     try:
    #         PennHospitals.objects.bulk_create(objects)
    #         # noinspection PyUnboundLocalVariable
    #         print(f'{entry.get("county")} hospital success')
    #     except IntegrityError:
    #         print(f'{entry.get("county")} hospital failure')


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
    nyt_data = nyt_data[nyt_data['fips'].isin(list(focus_fips.keys()))]

    # drop somerset and philly from data
    nyt_data = nyt_data[nyt_data['fips'] != '42101']
    nyt_data = nyt_data[nyt_data['fips'] != '42111']

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

        # drop somerset and philly from data
        nyt_live_data = nyt_live_data[nyt_live_data['fips'] != '42101']
        nyt_live_data = nyt_live_data[nyt_live_data['fips'] != '42111']

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

