import pandas as pd

from vid.models import (CasesDeathsNTY,
                        MetricsActNow,
                        PennDeaths,
                        PennCases,
                        PennHospitals)


def get_actnow_metrics(fips):
    act_now = pd.DataFrame(list(MetricsActNow.objects.filter(fips=fips).values()))
    act_now = act_now.set_index('date').sort_index()

    population = act_now.population.unique()[0]

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


def pa_data(county):
    cases = pd.DataFrame(list(PennCases.objects.filter(county=county).values()))
    cases = cases.set_index('date').sort_index()

    deaths = pd.DataFrame(list(PennDeaths.objects.filter(county=county).values()))
    deaths = deaths.set_index('date').sort_index()

    hospitals = pd.DataFrame(list(PennHospitals.objects.filter(county=county).values()))
    hospitals = hospitals.set_index('date').sort_index()

    fip_dict = {'Philadelphia': '42101',
                'Somerset': '42111'}
    fips = fip_dict[county]
    r_value, positive_rate, population = get_actnow_metrics(fips=fips)

    return cases, deaths, hospitals, r_value, positive_rate


if __name__ == '__main__':
    out = location_data('Somerset', 'Pennsylvania')
