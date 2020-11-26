import requests
import pandas as pd

from datetime import datetime
import time

from django.utils.timezone import make_aware
from django.db.utils import IntegrityError

from vid.models import Places, PennCaseDataDOH

api_key = '776e4ec57ee346d6a0a2a4abb6b006a8'
act_now_api = f'https://api.covidactnow.org/v2/county/42111.json?apiKey={api_key}'

penn_cases = 'https://data.pa.gov/resource/j72v-r42c.json'
penn_deaths = 'https://data.pa.gov/resource/fbgu-sqgp.json'
penn_hospital = 'https://data.pa.gov/resource/kayn-sjhx.json'

oklahoma_files = 'https://storage.googleapis.com/' \
                 'ok-covid-gcs-public-download/oklahoma_cases_county.csv'


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

    PennCaseDataDOH.objects.all().delete()

    # t2 = time.perf_counter()
    # print(f'{t2 - t1} seconds delete')

    for cases in county_data:
        objects = []
        for case in cases:
            date = datetime.strptime(case.get('date'), "%Y-%m-%dT%H:%M:%S.%f")
            aware_date = make_aware(date)
            obj = PennCaseDataDOH(cases=float(case.get('cases')),
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
            PennCaseDataDOH.objects.bulk_create(objects)
            print(f'{case.get("county")} success')
        except IntegrityError:
            print(f'{case.get("county")} failure')
