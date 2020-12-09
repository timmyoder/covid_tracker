from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT

from threading import Lock

from vid.page_server import location_data, pa_data
from vid.location_page import LocationPage

lock = Lock()

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


@cache_page(CACHE_TTL)
def somerset(request):
    cases, deaths, hospital, r_value, positive_rate = pa_data(county='Somerset')

    somerset_page = LocationPage('Somerset County, PA',
                                 cases=cases,
                                 deaths=deaths,
                                 r_value=r_value,
                                 hospital=hospital,
                                 positive_rate=positive_rate)

    with lock:
        somerset_page.create_case_plots()
        somerset_page.create_death_plots()
        somerset_page.create_hospital_plot()
        somerset_page.create_r_plot()
    return render(request, "location_page.jinja2", {"location_data": somerset_page})


@cache_page(CACHE_TTL)
def philly(request):
    cases, deaths, hospital, r_value, positive_rate = pa_data(county='Philadelphia')

    philly_page = LocationPage('Philadelphia County, PA',
                               cases=cases,
                               deaths=deaths,
                               r_value=r_value,
                               hospital=hospital,
                               positive_rate=positive_rate)

    with lock:
        philly_page.create_case_plots()
        philly_page.create_death_plots()
        philly_page.create_hospital_plot()
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


@cache_page(CACHE_TTL)
def dupage(request):
    cases, deaths, r_value, positive_rate = location_data('DuPage', 'Illinois')

    dupage_page = LocationPage('DuPage County, IL',
                               cases=cases,
                               deaths=deaths,
                               r_value=r_value,
                               positive_rate=positive_rate)
    with lock:
        dupage_page.create_case_plots()
        dupage_page.create_death_plots()
        dupage_page.create_r_plot()

    return render(request, "location_page.jinja2", {"location_data": dupage_page})


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

# todo: create comparison page


def home(request):
    return render(request, 'home.jinja2')


def sources(request):
    return render(request, 'sources.jinja2')
