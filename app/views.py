from django.core.paginator import Paginator
from django.shortcuts import render_to_response, redirect
from django.urls import reverse
from django.conf import settings
import csv
import urllib.parse

# Read-in data
data = []
with open(settings.BUS_STATION_CSV) as file:
    csv_reader = csv.DictReader(file)
    for i, line in enumerate(csv_reader):
        data.append(line)


def index(request):
    return redirect(reverse(bus_stations))


def bus_stations(request):
    page_num = request.GET.get('page', 1)
    paginator = Paginator(data, 10)
    # If the requested page number is more
    # than the total number of pages
    if int(page_num) > paginator.num_pages:
        page_num = paginator.num_pages
    page = paginator.page(page_num)
    obj_lst = page.object_list
    stations = [{'Name': obj['Name'], 'Street': obj['Street'], 'District': obj['District']} for obj in obj_lst]
    current_page = page.number
    # Prepare URLs for the previous and next pages
    prev_page_url = f'{reverse(bus_stations)}?{urllib.parse.urlencode({"page": current_page})}'
    next_page_url = f'{reverse(bus_stations)}?{urllib.parse.urlencode({"page": current_page})}'
    if page.has_next():
        next_page_dict = {'page': page.next_page_number()}
        params = urllib.parse.urlencode(next_page_dict)
        next_page_url = f'{reverse(bus_stations)}?{params}'
    if page.has_previous():
        prev_page_dict = {'page': page.previous_page_number()}
        params = urllib.parse.urlencode(prev_page_dict)
        prev_page_url = f'{reverse(bus_stations)}?{params}'
    return render_to_response('index.html', context={
        'bus_stations': stations,
        'current_page': current_page,
        'prev_page_url': prev_page_url,
        'next_page_url': next_page_url,
    })

