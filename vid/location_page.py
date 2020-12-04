"""Class to serve up location data to specific page"""
import vid.plotting


class LocationPage:
    """Class to serve up location data to specific page"""

    def __init__(self,
                 name,
                 cases,
                 deaths,
                 r_value=None,
                 hospital=None,
                 positive_rate=None):
        self.name = name
        self.cases = cases
        self.deaths = deaths
        self.hospital = hospital
        self.r_value = r_value
        self.positive_rate = f'{positive_rate*100:.2f}%'

        self.last_date = cases.index[-1].date()
        self.recent_cases = cases.iloc[-14:]
        self.recent_deaths = deaths.iloc[-14:]

        self.case_fig_html = ''
        self.death_fig_html = ''
        self.hospital_fig_html = ''
        self.r_fig_html = ''

        self.recent_cases_fig_html = ''
        self.recent_deaths_fig_html = ''
        self.hospital_avail_fig_html = ''

        self.cases_total = int(cases.cases_cume.iloc[-1])
        self.cases_2wk = int(self.recent_cases.cases.sum())
        self.cases_yesterday = int(cases.cases.iloc[-1])

        self.cases_total_100 = round(cases.cases_cume_rate.iloc[-1], 1)
        self.cases_2wk_100 = round(self.recent_cases.cases_rate.sum(), 1)
        self.cases_yesterday_100 = round(cases.cases_rate.iloc[-1], 1)

        self.deaths_total = int(deaths.deaths_cume.iloc[-1])
        self.deaths_2wk = int(self.recent_deaths.deaths.sum())
        self.deaths_yesterday = int(deaths.deaths.iloc[-1])

        self.deaths_total_100 = round(deaths.deaths_cume_rate.iloc[-1], 1)
        self.deaths_2wk_100 = round(self.recent_deaths.deaths_rate.sum(), 1)
        self.deaths_yesterday_100 = round(deaths.deaths_rate.iloc[-1], 1)

        self.hospital_ave = None
        self.hospital_percent = None

    def create_case_plots(self):
        self.cases = self.cases[self.cases['cases'] > 0]
        case_titles = {'figure': f'{self.name} Case Data',
                       'y': 'Daily Cases'}
        recent_titles = {'figure': f'{self.name} Case Data - Previous Two Weeks',
                         'y': 'Daily Cases'}
        self.case_fig_html = vid.plotting.plot_cases(self.cases.cases,
                                                     self.cases.cases_avg_new,
                                                     case_titles
                                                     )
        self.recent_cases_fig_html = vid.plotting.plot_cases(self.recent_cases.cases,
                                                             self.recent_cases.cases_avg_new,
                                                             recent_titles
                                                             )

    def create_death_plots(self):
        self.deaths = self.deaths[self.deaths['deaths'] > 0]

        death_titles = {'figure': f'{self.name} Death Data',
                        'y': 'Daily Deaths'}
        recent_titles = {'figure': f'{self.name} Death Data - Previous Two Weeks',
                         'y': 'Daily Deaths'}
        self.death_fig_html = vid.plotting.plot_deaths(self.deaths.deaths,
                                                       self.deaths.deaths_avg_new,
                                                       death_titles
                                                       )
        self.recent_deaths_fig_html = vid.plotting.plot_deaths(self.recent_deaths.deaths,
                                                               self.recent_deaths.deaths_avg_new,
                                                               recent_titles
                                                               )

    def create_hospital_plot(self):
        self.hospital_ave = self.hospital[['aii_total',
                                           'icu_total',
                                           'med_total',
                                           'covid_patients']].rolling(window=7).mean()

        self.hospital_percent = self.hospital[['aii_percent',
                                               'icu_percent',
                                               'med_percent']].iloc[-2:]

        self.hospital_percent.index = ['In Use', 'Available']
        self.hospital_percent.loc['In Use'] = 100 - self.hospital_percent.loc['Available']
        self.hospital_avail_fig_html = vid.plotting.plot_hospital_avail(self.hospital_percent)

        title = {'figure': 'Hospitalization Over Time',
                 'y': 'Daily Total Patients'}

        self.hospital_fig_html = vid.plotting.plot_hospitals(self.hospital['covid_patients'],
                                                             self.hospital_ave['covid_patients'],
                                                             title)

    def create_r_plot(self):
        title = {'figure': 'Infection Rate (r Value) Over Time',
                 'y': 'Modeled Infection Rate'}

        self.r_fig_html = vid.plotting.plot_rvalue(self.r_value,
                                                   title)
