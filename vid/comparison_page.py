"""Class to serve up location data to specific page"""
import vid.plotting


class ComparisonPage:
    """Class to serve up location data to specific page"""

    def __init__(self, case_list, death_list, county_names):
        self.case_list = case_list
        self.death_list = death_list
        self.county_names = county_names

        self.cases_fig_html = ''
        self.deaths_fig_html = ''
        self.recent_cases_fig_html = ''
        self.recent_deaths_fig_html = ''

        self.recent_cases = [case.iloc[-14:] for case in case_list]
        self.recent_deaths = [death.iloc[-14:] for death in death_list]

    def create_case_comparison_plots(self):
        titles = {'figure': f'All Counties 7-Day Average Case Data per 100k Residents',
                  'y': 'Daily Cases per 100k Residents'}

        self.cases_fig_html = vid.plotting.plot_comparison(self.case_list,
                                                           titles,
                                                           self.county_names)
        self.recent_cases_fig_html = vid.plotting.plot_comparison(self.recent_cases,
                                                                  titles,
                                                                  self.county_names)

    def create_death_comparison_plots(self):
        titles = {'figure': f'All Counties 7-Day Average Death Data per 100k Residents',
                  'y': 'Daily Deaths per 100k Residents'}

        self.deaths_fig_html = vid.plotting.plot_comparison(self.death_list,
                                                            titles,
                                                            self.county_names)
        self.recent_deaths_fig_html = vid.plotting.plot_comparison(self.recent_deaths,
                                                                   titles,
                                                                   self.county_names)
