import pandas as pd

from vid.models import (CasesDeathsNTY,
                        MetricsActNow,
                        AllNTY)

US_POPULATION = 328239523


def get_actnow_metrics(fips):
    act_now = pd.DataFrame(list(MetricsActNow.objects.filter(fips=fips).values()))
    act_now = act_now.set_index('date').sort_index()

    population = act_now.population.unique()[0]

    positivity_series = act_now['testPositivityRatio'].dropna()
    if positivity_series.empty:
        positive_rate = None
    else:
        positive_rate = act_now['testPositivityRatio'].dropna().iloc[-1]
    r_value = act_now['infectionRate']

    return r_value, positive_rate, population


def location_data(county, state):
    # get data for location from db
    nyt_data = pd.DataFrame(list(CasesDeathsNTY.objects.filter(county=county,
                                                               state=state).values()))
    nyt_data = nyt_data.set_index('date').sort_index()

    # calculate daily new cases/deaths based on cumulative totals
    nyt_data.rename(columns={'cases': 'cases_cume',
                             'deaths': 'deaths_cume'},
                    inplace=True)
    nyt_data['cases'] = nyt_data['cases_cume'].diff()
    nyt_data['deaths'] = nyt_data['deaths_cume'].diff()

    # calculate rolling 7-day averages
    nyt_data['cases_avg_new'] = nyt_data['cases'].rolling(window=7).mean()
    nyt_data['deaths_avg_new'] = nyt_data['deaths'].rolling(window=7).mean()

    fips = nyt_data.fips.unique()[0]

    r_value, positive_rate, population = get_actnow_metrics(fips=fips)

    per_100k_data = nyt_data[['cases',
                              'cases_avg_new',
                              'cases_cume',
                              'deaths',
                              'deaths_avg_new',
                              'deaths_cume']] / (float(population) / 100000)
    per_100k_data.rename(columns={'cases': 'cases_rate',
                                  'cases_avg_new': 'cases_avg_new_rate',
                                  'cases_cume': 'cases_cume_rate',
                                  'deaths': 'deaths_rate',
                                  'deaths_avg_new': 'deaths_avg_new_rate',
                                  'deaths_cume': 'deaths_cume_rate'},
                         inplace=True)

    nyt_data = nyt_data.join(per_100k_data)

    cases = nyt_data.drop(columns=['deaths',
                                   'deaths_avg_new',
                                   'deaths_cume',
                                   'deaths_rate',
                                   'deaths_avg_new_rate',
                                   'deaths_cume_rate'])
    deaths = nyt_data.drop(columns=['cases',
                                    'cases_avg_new',
                                    'cases_cume',
                                    'cases_rate',
                                    'cases_cume_rate',
                                    'cases_avg_new_rate',
                                    ])

    return cases, deaths, r_value, positive_rate


def us_data():
    # get data for location from db
    nyt_data = pd.DataFrame(list(AllNTY.objects.all().values()))
    nyt_data = nyt_data.set_index('date').sort_index()

    # calculate daily new cases/deaths based on cumulative totals
    nyt_data.rename(columns={'cases': 'cases_cume',
                             'deaths': 'deaths_cume'},
                    inplace=True)
    nyt_data['cases'] = nyt_data['cases_cume'].diff()
    nyt_data['deaths'] = nyt_data['deaths_cume'].diff()

    # calculate rolling 7-day averages
    nyt_data['cases_avg_new'] = nyt_data['cases'].rolling(window=7).mean()
    nyt_data['deaths_avg_new'] = nyt_data['deaths'].rolling(window=7).mean()

    per_100k_data = nyt_data[['cases',
                              'cases_avg_new',
                              'cases_cume',
                              'deaths',
                              'deaths_avg_new',
                              'deaths_cume']] / (US_POPULATION / 100000)
    per_100k_data.rename(columns={'cases': 'cases_rate',
                                  'cases_avg_new': 'cases_avg_new_rate',
                                  'cases_cume': 'cases_cume_rate',
                                  'deaths': 'deaths_rate',
                                  'deaths_avg_new': 'deaths_avg_new_rate',
                                  'deaths_cume': 'deaths_cume_rate'},
                         inplace=True)

    nyt_data = nyt_data.join(per_100k_data)

    cases = nyt_data.drop(columns=['deaths',
                                   'deaths_avg_new',
                                   'deaths_cume',
                                   'deaths_rate',
                                   'deaths_avg_new_rate',
                                   'deaths_cume_rate'])
    deaths = nyt_data.drop(columns=['cases',
                                    'cases_avg_new',
                                    'cases_cume',
                                    'cases_rate',
                                    'cases_cume_rate',
                                    'cases_avg_new_rate',
                                    ])
    return cases, deaths


def comparison_data(counties):
    case_list = []
    death_list = []

    for county in counties:
            cases, deaths, r_value, positive_rate = location_data(county[0],
                                                                  county[1])
            case_list.append(cases['cases_avg_new_rate'])
            death_list.append(deaths['deaths_avg_new_rate'])

    return case_list, death_list


if __name__ == '__main__':
    out = location_data('Somerset', 'Pennsylvania')
