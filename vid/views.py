from django.shortcuts import render
from threading import Lock

from vid.page_server import location_data, pa_data
from vid.location_page import LocationPage
import vid.get_data

lock = Lock()


def somerset(request):
    cases, deaths, hospital, r_value, positive_rate = pa_data(county='Somerset')

    somerset_page = LocationPage('Somerset',
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


def philly(request):
    cases, deaths, hospital, r_value, positive_rate = pa_data(county='Philadelphia')

    philly_page = LocationPage('Philadelphia',
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


def king(request):
    cases, deaths, r_value, positive_rate = location_data('King', 'Washington')

    king_page = LocationPage('King County',
                             cases=cases,
                             deaths=deaths,
                             r_value=r_value,
                             positive_rate=positive_rate)
    with lock:
        king_page.create_case_plots()
        king_page.create_death_plots()
        king_page.create_r_plot()

    return render(request, "location_page.jinja2", {"location_data": king_page})


def kane(request):
    cases, deaths, r_value, positive_rate = location_data('Kane', 'Illinois')

    kane_page = LocationPage('Kane, IL',
                             cases=cases,
                             deaths=deaths,
                             r_value=r_value,
                             positive_rate=positive_rate)
    with lock:
        kane_page.create_case_plots()
        kane_page.create_death_plots()
        kane_page.create_r_plot()

    return render(request, "location_page.jinja2", {"location_data": kane_page})


def dupage(request):
    cases, deaths, r_value, positive_rate = location_data('DuPage', 'Illinois')

    dupage_page = LocationPage('DuPage, IL',
                               cases=cases,
                               deaths=deaths,
                               r_value=r_value,
                               positive_rate=positive_rate)
    with lock:
        dupage_page.create_case_plots()
        dupage_page.create_death_plots()
        dupage_page.create_r_plot()

    return render(request, "location_page.jinja2", {"location_data": dupage_page})


def okc(request):
    cases, deaths, r_value, positive_rate = location_data('Oklahoma', 'Oklahoma')

    okc_page = LocationPage('Oklahoma County',
                            cases=cases,
                            deaths=deaths,
                            r_value=r_value,
                            positive_rate=positive_rate)
    with lock:
        okc_page.create_case_plots()
        okc_page.create_death_plots()
        okc_page.create_r_plot()

    return render(request, "location_page.jinja2", {"location_data": okc_page})


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
