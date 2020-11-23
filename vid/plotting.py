import matplotlib
import numpy as np
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.ioff()
import mpld3

import warnings

title_font = {'fontsize': 18,
              }
axis_font = {'fontsize': 14}


def plot_cases(case_data, avg_case_data, titles):
    fig = plt.figure()

    plt.bar(case_data.index,
            case_data,
            alpha=.6,
            color='tab:gray',
            label='Single Day')
    plt.plot(avg_case_data,
             color='tab:red',
             lw=3,
             label='7 Day Average')
    plt.title(titles['figure'],
              fontdict=title_font)
    plt.ylabel(titles['y'],
               fontdict=axis_font)
    fig.autofmt_xdate(rotation=45)
    plt.legend()
    html_str = mpld3.fig_to_html(fig)

    return html_str


def plot_deaths(death_data, titles):
    fig = plt.figure()

    plt.bar(death_data.index,
            death_data,
            lw=3,
            color='tab:red')

    plt.title(titles['figure'],
              fontdict=title_font)
    plt.ylabel(titles['y'],
               fontdict=axis_font)
    fig.autofmt_xdate(rotation=45)
    html_str = mpld3.fig_to_html(fig)

    return html_str


def plot_hospital_avail(percentage_data):
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')

        fig, ax = plt.subplots()

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
    fig = plt.figure()

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
    plt.ylabel(titles['y'],
               fontdict=axis_font)
    fig.autofmt_xdate(rotation=45)
    plt.legend()
    html_str = mpld3.fig_to_html(fig)

    return html_str