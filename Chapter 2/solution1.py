import csv  
import sys
import time
from numbers import Number
from typing import Dict, List, Tuple
from math import asin, cos, pi, sin, sqrt

def measure_execution_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f'Function {func} Execution time: {end_time - start_time} seconds')
        return result
    return wrapper

def load_csv(filename:str = 'worldcities.csv')->Dict:
    with open(filename) as csvfile:  
        list_of_cities = csv.DictReader(csvfile)
        return { d['city_ascii']:d for d in list_of_cities}  

def load_city_args(args:List, cities: List)->Dict:
    n = len(args)
    cities_list = []
    for i in range(1, n):
        if args[i] in cities.keys():
            cities_list.append(cities[args[i]])
    return cities_list

def cities_into_tuples(cities:List)->List:
    cities_list = []
    total_cities = len(cities)
    for i in range(0, total_cities):
        if i+1 < total_cities:
            cities_list.append((cities[i], cities[i+1],))
    return cities_list

def great_circle_distance(src_dest: Tuple)->Number:
    source = src_dest[0]
    dest = src_dest[1]
    lat1 = abs(float(source['lat'])*pi/180)
    lat2 = abs(float(dest['lat'])*pi/180)
    lon1 = abs(float(source['lng'])*pi/180)
    lon2 = abs(float(dest['lng'])*pi/180)
    distance = 2*asin(sqrt((sin((lat1-lat2)/2))**2 + cos(lat1)*cos(lat2)*(sin((lon1-lon2)/2))**2)) 
    distance = distance*180*60/pi
    return distance

@measure_execution_time
def calculate_path_distance(cities: List)->Number:
    total = 0
    for t in cities:
        d = great_circle_distance(t)
        print(f'From: {t[0]['city_ascii']} to: {t[1]['city_ascii']}, distance: {d} nm')
        total = total + d
    return total

if __name__ == '__main__':
    cities = load_csv('worldcities.csv')
    candidate_cities = load_city_args(sys.argv, cities)
    cities_to_be_visited = cities_into_tuples(candidate_cities)
    total = calculate_path_distance(cities_to_be_visited)
    print(f'Total distance: {total}nm')