from constant import DEV_KEY, mkad_points
from shapely.geometry import Polygon, Point
from math import cos, sqrt
import requests
from lxml import etree
from flask import (
    Blueprint, render_template, request
)
import logging

bp = Blueprint('bp', __name__, template_folder='templates')


@bp.route('/calc', methods=('GET', 'POST'))
def calc():
    if request.method == 'POST':
        address = request.form['address']
        output = make_request(address)
        logging.basicConfig(filename='request_log.log', level=logging.INFO)
        logging.info('Entered address --->' + address + ' ' + output)
        logging.info('Received answer' + output)
        return render_template('result.html', output=output)
    return render_template('main.html')


def make_request(address: str) -> str:
    """function that takes entered address from POST HTTP request
    return a message to output to user
    Function uses Point, Polygon from shapely.geometry to search point in
    MKAD"""
    try:
        coordinates = get_coordinates(create_params(address))
        mkad_polygon = Polygon(tuple(mkad_points))
        if mkad_polygon.contains(Point(coordinates)):
            message = 'Entered address is in MKAD-area'
        else:
            min_distance = count_min_distance(coordinates)
            message = 'Entered address is ' + str(round(min_distance, 3)) + \
                      'km away from MKAD'
    except Exception:
        message = "Something goes wrong, try another one"
    return message


def count_min_distance(coordinates: tuple) -> float:
    """function that takes longitude and latitude tuple
    count min_distance from MKAD to that point in kilometers"""
    min_distance = 0
    for longitude, latitude in mkad_points:
        average_latitude = (latitude + coordinates[1]) / 2
        distance = sqrt(((longitude - coordinates[0]) ** 2) *
                        (111.32137777 ** 2) * cos(average_latitude) +
                        ((latitude - coordinates[1]) ** 2) *
                        (111.134861111 ** 2))
        if distance < min_distance or min_distance == 0:
            min_distance = distance
    return min_distance


def get_coordinates(params: dict) -> tuple:
    """function that takes parameters and do GET request to GEOKODER
       return from request needed coordinates of address"""
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 ('
                      'KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36',
        'accept': '*/*'}
    r = requests.get('https://geocode-maps.yandex.ru/1.x/', headers=headers,
                     params=params)
    root = etree.fromstring(bytes(r.text, encoding='utf-8'))
    longitude, latitude = tuple(root[0][1][0][4][0].text.split(' '))
    coordinates = (float(longitude), float(latitude))
    return coordinates


def create_params(address: str) -> dict:
    """function that create parameters to GET request to GEOKODER
       take address
       return dictionary of parameters"""
    address_to_string = address.replace(" ", "+")
    params = {'apikey': DEV_KEY,
              'geocode': address_to_string}
    return params
