import pandas as pd

from vid.models import CasesDeathsNTY


def nyt_location_data(county, state):

    # get data for location from db
    df = pd.DataFrame(list(CasesDeathsNTY.objects.filter(county=county,
                                                         state=state).values()))
    df = df.set_index('date').sort_index()

    df.rename(columns={'cases': 'cases_cume',
                       'deaths': 'deaths_cume'},
              inplace=True)
    df['cases'] = df['cases_cume'].diff()
    df['deaths'] = df['deaths_cume'].diff()

    df['cases_avg_new'] = df['cases'].rolling(window=7).mean()
    df['deaths_avg_new'] = df['deaths'].rolling(window=7).mean()

    return df

if __name__ == '__main__':
    out = nyt_location_data('Somerset', 'Pennsylvania')
