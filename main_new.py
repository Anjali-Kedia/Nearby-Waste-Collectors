from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import ssl
import re
import math
from continents import *
import folium
import random

ssl._create_default_https_context = ssl._create_unverified_context
geolocator = Nominatim(user_agent="Waste-Collectors-Nearby")#need to change

#1.newspapers,old books,cardboard boxes
#2.kitchen waste
#3.metal waste
#4.glass items
#5.plastic
#6.e-waste
def read_file(path):
    """
    (str) -> (dict)
    Return a dictionary of parsed collectors from the file
    """
    print('\nReading file. Wait for 5-7 seconds ...')
    key_lines = {}
    i = 0
    with open(path, encoding='utf-8', errors='ignore') as file:
        for line in file:
            i += 1
            line = line.strip()
            if not line:
                continue
            try:
                option = int(line.split(' (')[1].replace('\t', ' ')
                           .split('/')[0].split(')')[0])
                title = line.split(' (')[0].replace('(' + str(option) + ')', '')
                loc = line.replace("\t", " ").split(") ")[1]
                if option in key_lines.keys():
                    key_lines[option].add((title, loc))
                else:
                    key_lines[option] = set()
                    key_lines[option].add((title, loc))
            except Exception as e:
                continue
    print("\nTotal of %s collectors parsed\n" % i)
    return key_lines


def filter_location(location):
    """ (str) -> str
    Filter input string from such characters as
    parentheses and blank symbols
    >>> filter_location("United Kingdom {(UK)}")
    'United Kingdom'
    """
    location = re.sub("[(].*?[)]", "", location)
    location = re.sub("[{].*?[}]", "", location)
    location = location.replace("\t", "")
    location = location.replace("\n", " ")
    location = location.replace("\r", " ")
    location = ' '.join(location.split())
    return location


def get_country_and_city(location):
    """ (str) -> (str, str)
    Get country and city information from the given
    input location as one string
    >>> get_country_and_city("23, Some Road, Houston, Texas, USA")
    ('USA', 'Texas')
    """
    location = filter_location(location).split(", ")
    country = location[-1]
    """
    if country == "United States of America":
        country = "USA"
    elif country == "United Kingdom":
        country = "UK"
        """
    if not location[-2].isalpha() and len(location) > 2:
        city = location[-3]
    else:
        city = location[-2]
    return country, city


def find_collectors(option, lat, lon, location, deep_search=False, data=None):
    """ (int, float, float, Location, Bool, set) -> set
    Prefilter collectors by their locations using three main categories:
    city area, country area, and continent area
    """
    if not location.address:
        return set()
    country_input, city_input = get_country_and_city(location.address)
    near_collectors_by_country = set()
    near_collectors_by_city = set()
    collectors_in_near_countries = set()
    try:
        continent_input = ALL_COUNTRIES[country_input]
    except:
        if deep_search:
            return set()
        continent_input = ''
    if not deep_search:
        print("Input Location:", country_input, city_input)
        data = read_file(path="locations2.list")
    length_dict = [len(value) for key, value in data.items()]
    total_checked = 0
    no_info = 0
    if option not in data:
        print('No collectors for the selected option!')
        return set()
    for person_loc in data[option]:
        person, loc = person_loc
        loc = filter_location(loc)
        try:
            total_checked += 1
            collector_country, collector_city = get_country_and_city(loc)
            if deep_search:
                if collector_country in ALL_CONTINENTS[continent_input]:
                    collectors_in_near_countries.add((person, loc))
                continue
            if city_input == collector_city:
                near_collectors_by_city.add((person, loc))
            elif country_input == collector_country:
                near_collectors_by_country.add((person, loc))
        except Exception as e:
            no_info += 1

    if deep_search:
        return collectors_in_near_countries
    if len(near_collectors_by_country) < 15:
        print("Too few collectors found in the area, starting deep search")
        continent_search = find_collectors(option, lat, lon, location, True, data)
        continent_result = "Total collectors in %s: %s" % \
                           (continent_input, len(continent_search))
    else:
        continent_search = set()
        continent_result = ''
    print('-' * 55)
    print('Found %s collectors in %s \n ' % (total_checked - no_info, option))
    print("Total collectors in %s: %s \n " %
          (city_input, len(near_collectors_by_city)))
    print("Total collectors in %s: %s \n" %
          (country_input, len(near_collectors_by_country)))
    if continent_result:
        print(continent_result)
    print('-' * 55)

    if 3 <= len(near_collectors_by_city) <= len(near_collectors_by_country):
        return near_collectors_by_city
    elif len(near_collectors_by_country) < len(near_collectors_by_city) \
            and len(near_collectors_by_country) != 0:
        return near_collectors_by_country
    elif 1 <= len(near_collectors_by_country) < 15:
        if len(continent_search) != 0:
            return continent_search
        else:
            return near_collectors_by_country
    elif len(near_collectors_by_country) >= 15:
        return near_collectors_by_country
    else:
        return continent_search


def calculate_distance(x1, y1, x2, y2):
    """ (float, float, float, float) -> float
    Calculate distance between two coordinates on the map
    >>> calculate_distance(43.45, 51.1345, 12.456, -50.34)
    106.1023194197469
    """
    dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return dist


def select_the_nearest(collectors, lat_inp, long_inp):
    """ (set, float, float) -> list
    Get a final set of collectors near the given location
    """
    print("Calculating the nearest places. "
          "It may take up to %s minutes" % round(len(collectors) / 120, 2))
    distance_lst = []
    collectors_lst = []
    for collector_tuple in collectors:
        try:
            title, loc = collector_tuple
            location = geolocator.geocode(loc, language='en', timeout=3)
            lat = location.latitude
            long = location.longitude
            distance = calculate_distance(lat_inp, long_inp, lat, long)
            distance_lst.append(distance)
            distance_lst.sort()
            ind = distance_lst.index(distance)
            collectors_lst.insert(ind, (title, (lat, long)))
        except:
            continue
    return collectors_lst[:10]


def display_places(collectors, lat_inp, long_inp, option):
    """ (set, float, float, int) -> None
    Display the final set of movies on the map and generate the final
    file.
    """
    map = folium.Map(location=[lat_inp, long_inp], zoom_start=8)

    fg_list = []
    fg = folium.FeatureGroup(name='Your Location')
    fg.add_child(folium.Marker(location=[lat_inp, long_inp],
                               popup='Your Location',
                               icon=folium.Icon(icon='user', color='red'),
                               ))
    fg_list.append(fg)

    fg = folium.FeatureGroup(name='Collectors nearby in %s' % option)
    locations_used = []
    for collector in collectors:
        title, loc = collector
        while loc in locations_used:
            r_earth = 6378  # km
            dy = random.choice([-1, 1, 2, -2, 3, -3, 4, -4])
            dx = random.choice([-1, 1, 2, -2, 3, -3, 4, -4])
            new_latitude = loc[0] + (dy / r_earth) * (180 / math.pi)
            new_longitude = loc[1] + (dx / r_earth) * (180 / math.pi) \
                / math.cos(loc[0] * math.pi / 180)
            loc = (new_latitude, new_longitude)
        locations_used.append(loc)
        fg.add_child(folium.Marker(location=list(loc),
                                   popup=title,
                                   icon=folium.Icon(icon='pushpin'),
                                   ))
    fg_list.append(fg)

    fg = folium.FeatureGroup(name='World Capitals', show=False)

    with open('capitals.csv', encoding='utf-8', errors='ignore') as file:
        for line in file:
            capital = line.split(',')
            fg.add_child(folium.Marker(location=[capital[2], capital[3]],
                                       popup=capital[0] + capital[1],
                                       icon=folium.Icon(icon='triangle-bottom',
                                                        color='blue'),
                                       ))

    fg_list.append(fg)

    for i in fg_list:
        map.add_child(i)

    map.add_child(folium.LayerControl())
    map.save("map_%s_collectors_map.html" % option)

def find_latlong(address):
    geocoder= Nominatim(user_agent="Waster-Collectors-Nearby")   
    geocode = RateLimiter(geocoder.geocode, min_delay_seconds = 1,   return_value_on_exception = None) 
    # adding 1 second padding between calls

    location= geocode(address)
    result=(location.latitude,location.longitude)
    return result


if __name__ == '__main__':
    try:
        option = int(input("Please enter from below :\n1.newspapers,old books,cardboard boxes \n2.kitchen waste\n3.metal waste\n4.glass items\n5.plastic\n6.e-waste\n"))
        print("enter address: ")
        place = find_latlong(input())

        while place:
            lat = place[0]
            lon = place[1]
            location = geolocator.reverse("%s, %s" % (lat, lon),
                                          language='en', timeout=3)
            try:
                # if location doesn't exist, the code
                # below will throw exception
                address = location.address
            except Exception as e:
                print("Wrong coordinates!")

            names = find_collectors(option, lat, lon, location)
            if len(names) == 0:
                print('-' * 55)
                print('Unfortunately, it isn\'t possible '
                      'to find collectors nearby ')
                print('for your location and year picked :()')
                print('-' * 55)
            else:
                names = list(names)[:240]
                names = select_the_nearest(names, lat, lon)
                display_places(names, lat, lon, option)
                print("\nFinished. Please have look at the map "
                      "map_%s_collectors_map.html" % option)
            break
    except ValueError:
        print("Wrong input data! Try one more time!")