from django.shortcuts import render
from threading import Lock

from vid.page_server import nyt_location_data
from vid.location_page import LocationPage
import vid.get_data

lock = Lock()


def somerset(request):
    cases, deaths, hospital = vid.get_data.get_penn_data(county='Somerset')

    somerset_page = LocationPage('Somerset',
                                 cases=cases,
                                 deaths=deaths,
                                 r_value=0,
                                 hospital=hospital)

    with lock:
        somerset_page.create_case_plots()
        somerset_page.create_death_plots()
        somerset_page.create_hospital_plot()
    return render(request, "location_page.jinja2", {"location_data": somerset_page})


def philly(request):
    cases, deaths, hospital = vid.get_data.get_penn_data(county='Philadelphia')

    philly_page = LocationPage('Philadelphia',
                               cases=cases,
                               deaths=deaths,
                               r_value=0,
                               hospital=hospital)

    with lock:
        philly_page.create_case_plots()
        philly_page.create_death_plots()
        philly_page.create_hospital_plot()
    return render(request, "location_page.jinja2", {"location_data": philly_page})

def king(request):
    cases_and_deaths = nyt_location_data('King', 'Washington')




def home(request):
    return render(request, 'home.jinja2')
