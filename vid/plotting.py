import matplotlib
import numpy as np

matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.ioff()
import mpld3

import warnings

warnings.filterwarnings("ignore", category=matplotlib.cbook.mplDeprecation)

title_font = {'fontsize': 18,
              }
axis_font = {'fontsize': 14}


def plot_cases(case_data, avg_case_data, titles):
    fig = plt.figure(figsize=(10, 6))

    plt.bar(case_data.index,
            case_data,
            alpha=.6,
            color='tab:gray',
            label='Single Day')
    plt.plot(avg_case_data,
             color='tab:red',
             lw=3,
             label='7 Day Average')

    points = plt.scatter(avg_case_data.index,
                         avg_case_data,
                         color='none')
    labels = [f'Average {val:.1f}' for val in avg_case_data.values]
    tooltip = mpld3.plugins.PointHTMLTooltip(points, labels)
    mpld3.plugins.connect(fig, tooltip)

    plt.title(titles['figure'],
              fontdict=title_font)
    plt.ylabel(titles['y'],
               fontdict=axis_font)
    fig.autofmt_xdate(rotation=45)
    plt.legend()
    html_str = mpld3.fig_to_html(fig)

    return html_str


def plot_deaths(death_data, death_ave, titles):
    fig = plt.figure(figsize=(10, 6))

    plt.bar(death_data.index,
            death_data,
            color='tab:red',
            alpha=.6,
            label='Single Day'
            )

    plt.plot(death_ave,
             color='tab:red',
             lw=3,
             label='7 Day Average')

    points = plt.scatter(death_ave.index,
                         death_ave,
                         color='none')
    labels = [f'Average {val:.1f}' for val in death_ave.values]
    tooltip = mpld3.plugins.PointHTMLTooltip(points, labels)
    mpld3.plugins.connect(fig, tooltip)

    plt.title(titles['figure'],
              fontdict=title_font)
    plt.ylabel(titles['y'],
               fontdict=axis_font)
    fig.autofmt_xdate(rotation=45)

    plt.legend()
    html_str = mpld3.fig_to_html(fig)

    return html_str


def plot_hospital_avail(percentage_data):
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')

        fig, ax = plt.subplots(figsize=(10, 6))

        # The position of the bars on the x-axis
        r = np.arange(len(percentage_data.columns))

        avail = np.array(percentage_data.loc['Available'])
        in_use = np.array(percentage_data.loc['In Use'])
        bed_types = ('AII', 'ICU', 'MED')

        barWidth = 1
        # plot bars

        ax.bar(r,
               avail,
               bottom=in_use,
               color='tab:green',
               edgecolor='white',
               width=barWidth,
               label="Available")
        ax.bar(r,
               in_use,
               color='tab:red',
               edgecolor='white',
               width=barWidth,
               label="In Use")
        plt.legend()
        plt.title('Current Hospital Capacity')
        ax.set_xticks(r)
        ax.set_xticklabels(bed_types)
        # plt.xticks(ticks=r, labels=bed_types, fontweight='bold')
        ax.set_ylabel("Percent of Beds")
        ax.set_xlabel(bed_types)

        html_str = mpld3.fig_to_html(fig)

    return html_str


def plot_hospitals(covid_daily,
                   covid_average,
                   titles):
    fig = plt.figure(figsize=(10, 6))

    plt.bar(covid_daily.index,
            covid_daily,
            alpha=.65,
            color='tab:gray',
            label='Single Day - Covid Patients')
    plt.plot(covid_average,
             color='tab:red',
             lw=3,
             label='7 Day Average - Covid Patients')
    plt.title(titles['figure'],
              fontdict=title_font)
    points = plt.scatter(covid_average.index,
                         covid_average,
                         color='none')
    labels = [f'Average {val:.1f}' for val in covid_average.values]
    tooltip = mpld3.plugins.PointHTMLTooltip(points, labels)
    mpld3.plugins.connect(fig, tooltip)
    plt.ylabel(titles['y'],
               fontdict=axis_font)
    fig.autofmt_xdate(rotation=45)
    plt.legend()
    html_str = mpld3.fig_to_html(fig)

    return html_str


def plot_rvalue(r_series, titles):
    r_series = r_series.dropna()

    fig = plt.figure(figsize=(10, 6))

    plt.plot(r_series.index,
             r_series,
             lw=3,
             color='tab:orange')

    # add scatter plot with no color for labels
    points = plt.scatter(r_series.index,
                         r_series,
                         color='none')
    labels = [f'{value:.2f}' for value in r_series.values]
    tooltip = mpld3.plugins.PointHTMLTooltip(points, labels)
    mpld3.plugins.connect(fig, tooltip)

    plt.plot(r_series.index,
             np.ones(len(r_series)),
             alpha=.6,
             color='tab:gray',
             linestyle='--')

    plt.title(titles['figure'],
              fontdict=title_font)
    plt.ylabel(titles['y'],
               fontdict=axis_font)
    fig.autofmt_xdate(rotation=45)
    html_str = mpld3.fig_to_html(fig)

    return html_str


def plot_comparison(list_of_counties, titles, labels):
    fig = plt.figure(figsize=(10, 6))

    colors = ['tab:blue',
              'tab:orange',
              'tab:green',
              'tab:red',
              'tab:purple',
              'tab:cyan',
              'tab:gray',
              'tab:brown']

    for ind, county in enumerate(list_of_counties):
        plt.plot(county.index,
                 county,
                 lw=2,
                 color=colors[ind],
                 label=labels[ind])
        # add scatter plot with no color for labels
        points = plt.scatter(county.index,
                             county,
                             color='none')
        tip_labels = [f'{labels[ind]}: {value:.2f}' for value in county.values]
        tooltip = mpld3.plugins.PointHTMLTooltip(points, tip_labels)
        mpld3.plugins.connect(fig, tooltip)

    plt.legend(bbox_to_anchor=(1.04, 0.5), loc="center left", borderaxespad=0)
    plt.subplots_adjust(right=0.8)

    plt.title(titles['figure'],
              fontdict=title_font,
              )
    plt.ylabel(titles['y'],
               fontdict=axis_font)
    fig.autofmt_xdate(rotation=45)
    html_str = mpld3.fig_to_html(fig)

    return html_str
