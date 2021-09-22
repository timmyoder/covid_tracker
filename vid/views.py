from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT

from threading import Lock

from vid.page_server import location_data, comparison_data, us_data
from vid.location_page import LocationPage
from vid.comparison_page import ComparisonPage

lock = Lock()

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


@cache_page(CACHE_TTL)
def somerset(request):
    cases, deaths, r_value, positive_rate = location_data('Somerset', 'Pennsylvania')

    somerset_page = LocationPage('Somerset County, PA',
                                 cases=cases,
                                 deaths=deaths,
                                 r_value=r_value,
                                 positive_rate=positive_rate)

    with lock:
        somerset_page.create_case_plots()
        somerset_page.create_death_plots()
        somerset_page.create_r_plot()
    return render(request, "location_page.jinja2", {"location_data": somerset_page})


@cache_page(CACHE_TTL)
def philly(request):
    cases, deaths, r_value, positive_rate = location_data('Philadelphia', 'Pennsylvania')

    philly_page = LocationPage('Philadelphia County, PA',
                               cases=cases,
                               deaths=deaths,
                               r_value=r_value,
                               positive_rate=positive_rate)

    with lock:
        philly_page.create_case_plots()
        philly_page.create_death_plots()
        philly_page.create_r_plot()
    return render(request, "location_page.jinja2", {"location_data": philly_page})


@cache_page(CACHE_TTL)
def king(request):
    cases, deaths, r_value, positive_rate = location_data('King', 'Washington')

    king_page = LocationPage('King County, WA',
                             cases=cases,
                             deaths=deaths,
                             r_value=r_value,
                             positive_rate=positive_rate)
    with lock:
        king_page.create_case_plots()
        king_page.create_death_plots()
        king_page.create_r_plot()

    return render(request, "location_page.jinja2", {"location_data": king_page})


@cache_page(CACHE_TTL)
def kane(request):
    cases, deaths, r_value, positive_rate = location_data('Kane', 'Illinois')

    kane_page = LocationPage('Kane County, IL',
                             cases=cases,
                             deaths=deaths,
                             r_value=r_value,
                             positive_rate=positive_rate)
    with lock:
        kane_page.create_case_plots()
        kane_page.create_death_plots()
        kane_page.create_r_plot()

    return render(request, "location_page.jinja2", {"location_data": kane_page})


# @cache_page(CACHE_TTL)
# def dupage(request):
#     cases, deaths, r_value, positive_rate = location_data('DuPage', 'Illinois')
#
#     dupage_page = LocationPage('DuPage County, IL',
#                                cases=cases,
#                                deaths=deaths,
#                                r_value=r_value,
#                                positive_rate=positive_rate)
#     with lock:
#         dupage_page.create_case_plots()
#         dupage_page.create_death_plots()
#         dupage_page.create_r_plot()
#
#     return render(request, "location_page.jinja2", {"location_data": dupage_page})


@cache_page(CACHE_TTL)
def okc(request):
    cases, deaths, r_value, positive_rate = location_data('Oklahoma', 'Oklahoma')

    okc_page = LocationPage('Oklahoma County, OK',
                            cases=cases,
                            deaths=deaths,
                            r_value=r_value,
                            positive_rate=positive_rate)
    with lock:
        okc_page.create_case_plots()
        okc_page.create_death_plots()
        okc_page.create_r_plot()

    return render(request, "location_page.jinja2", {"location_data": okc_page})


@cache_page(CACHE_TTL)
def cleveland(request):
    cases, deaths, r_value, positive_rate = location_data('Cleveland', 'Oklahoma')

    cleveland_page = LocationPage('Cleveland County, OK',
                                  cases=cases,
                                  deaths=deaths,
                                  r_value=r_value,
                                  positive_rate=positive_rate)
    with lock:
        cleveland_page.create_case_plots()
        cleveland_page.create_death_plots()
        cleveland_page.create_r_plot()

    return render(request, "location_page.jinja2", {"location_data": cleveland_page})


@cache_page(CACHE_TTL)
def los_angeles(request):
    cases, deaths, r_value, positive_rate = location_data('Los Angeles', 'California')

    los_angeles_page = LocationPage('Los Angeles County, CA',
                                    cases=cases,
                                    deaths=deaths,
                                    r_value=r_value,
                                    positive_rate=positive_rate)
    with lock:
        los_angeles_page.create_case_plots()
        los_angeles_page.create_death_plots()
        los_angeles_page.create_r_plot()

    return render(request, "location_page.jinja2", {"location_data": los_angeles_page})


@cache_page(CACHE_TTL)
def comparison(request):
    counties = [('Somerset', 'Pennsylvania'),
                ('Philadelphia', 'Pennsylvania'),
                ('Los Angeles', 'California'),
                ('Cleveland', 'Oklahoma'),
                ('Oklahoma', 'Oklahoma'),
                # ('DuPage', 'Illinois'),
                ('Kane', 'Illinois'),
                ('King', 'Washington')]

    cases, deaths = comparison_data(counties=counties)
    us_cases, us_deaths = us_data()

    counties = ['Somerset, PA',
                'Philadelphia, PA',
                'Los Angeles, CA',
                'Cleveland, OK',
                'Oklahoma, OK',
                # 'DuPage, IL',
                'Kane, IL',
                'King, WA']

    comparison_page = ComparisonPage(case_list=cases,
                                     death_list=deaths,
                                     us_cases=us_cases['cases_avg_new_rate'],
                                     us_deaths=us_deaths['deaths_avg_new_rate'],
                                     county_names=counties)
    with lock:
        comparison_page.create_case_comparison_plots()
        comparison_page.create_death_comparison_plots()

    return render(request, "comparison.jinja2", {"comparison": comparison_page})


def home(request):
    return render(request, 'home.jinja2')


def sources(request):
    return render(request, 'sources.jinja2')
