"""Class to serve up location data to specific page"""
import vid.plotting
import datetime
import pandas as pd

class ComparisonPage:
    """Class to serve up location data to specific page"""

    def __init__(self, us_cases, us_deaths, case_list, death_list, county_names):
        self.us_cases = us_cases
        self.us_death = us_deaths
        self.case_list = case_list
        self.death_list = death_list
        self.county_names = county_names

        self.cases_fig_html = ''
        self.deaths_fig_html = ''
        self.recent_cases_fig_html = ''
        self.recent_deaths_fig_html = ''

        today = datetime.date.today()
        two_weeks = pd.Timestamp(today - datetime.timedelta(days=14))

        self.recent_cases_us = us_cases.loc[two_weeks:]
        self.recent_deaths_us = us_deaths.loc[two_weeks:]
        self.recent_cases = [case.loc[two_weeks:] for case in case_list]
        self.recent_deaths = [death.loc[two_weeks:] for death in death_list]

    def create_case_comparison_plots(self):
        titles = {'figure': f'All Counties 7-Day Average Case Data per 100k Residents',
                  'y': 'Daily Cases per 100k Residents'}

        self.cases_fig_html = vid.plotting.plot_comparison(self.case_list,
                                                           self.us_cases,
                                                           titles,
                                                           self.county_names)
        self.recent_cases_fig_html = vid.plotting.plot_comparison(self.recent_cases,
                                                                  self.recent_cases_us,
                                                                  titles,
                                                                  self.county_names)

    def create_death_comparison_plots(self):
        titles = {'figure': f'All Counties 7-Day Average Death Data per 100k Residents',
                  'y': 'Daily Deaths per 100k Residents'}

        self.deaths_fig_html = vid.plotting.plot_comparison(self.death_list,
                                                            self.us_death,
                                                            titles,
                                                            self.county_names)
        self.recent_deaths_fig_html = vid.plotting.plot_comparison(self.recent_deaths,
                                                                   self.recent_deaths_us,
                                                                   titles,
                                                                   self.county_names)
