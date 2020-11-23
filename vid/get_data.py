import requests
import pandas as pd

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

