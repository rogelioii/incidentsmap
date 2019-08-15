import json
import requests
import names
import random
import pytz
from .models import Parcel, Incident 
from datetime import datetime



class Enricher(object):
    def __init__(self, data):
        self.data = data
        self.weather_lat_long = []
        self.parcel_polygon_list = []

        self._set_weather_lat_long()
        self._set_parcel_polygon_list()

        print('Enricher construct.')
        print('weather: {}'.format(self.weather_lat_long))
        print('parcel: {}'.format(self.parcel_polygon_list))


    def enrich(self, _model_instance):
        if isinstance(_model_instance, Parcel):
            self._enrich_parcel(_model_instance)
        elif isinstance(_model_instance, Incident):
            self._enrich_incident(_model_instance)
        else:
            raise Exception('enrich does not support {}'.format(type(_model_instance)))

    def _iso_to_utc_epoch(self, iso):
        # TODO: make this timezone calculation better.
        tz = pytz.timezone('UTC')
        offset = 0 - int(iso[:-3][-3:]) * 3600
        dt_with_tz = tz.localize(datetime.strptime(iso[:-6], '%Y-%m-%dT%H:%M:%S'), is_dst=None)
        ts = (dt_with_tz - datetime(1970, 1, 1, tzinfo=pytz.utc)).total_seconds() + offset
        return int(ts)
    
    def _enrich_incident(self, incident):
        flat_points = ','.join([str(s) for s in self.weather_lat_long])
        weather_ts = incident.incident_event_opened
        url = 'https://api.darksky.net/forecast/971bc3c7f3e0e07dc4982e2aa9f013f9/{},{}?exclude=currently,flags,daily'.format(flat_points, weather_ts)
        print('_enrich_incident request url is: {}'.format(url))
        response = requests.get(url)
        print('_enrich_incident response is: {}'.format(response.json()))
        
        # check each hourly and check the weather of the closest half-hour to incident
        try:
            body = response.json()
        except Exception as e:
            raise e

        incident_epoch = self._iso_to_utc_epoch(weather_ts)

        if 'hourly' in body and 'data' in body['hourly']:
            incident.weather_description = 'No Weather Data'
            for hour in body['hourly']['data']:
                if abs(hour['time'] - incident_epoch) < 30:
                    # found the incident weather
                    incident.weather_description = self._get_weather_description(hour)
                    break

    
    def _get_weather_description(self, weather_data):
        # TODO: add dew point and apparent temp later.
        temperature = weather_data['temperature']
        summary = weather_data['summary']
        p_intensity = weather_data['precipIntensity']
        p_probability = weather_data['precipProbability']
        humidity = weather_data['humidity']
        pressure = weather_data['pressure']
        wspeed = weather_data['windSpeed']
        wgust = weather_data['windGust']
        wbearing = weather_data['windBearing']
        cloudcover = weather_data['cloudCover']
        uvindex = weather_data['uvIndex']
        visibility = weather_data['visibility']
        return '''
        {} and {}
        PrecipIntensity: {}
        PrecipProbability: {}
        Humidity: {}
        Pressure: {}
        Wind Speed: {}
        Wind Gust: {}
        Wind Bearing: {}
        Cloud Cover: {}
        UV Index: {}
        Visibility: {}

        '''.format(temperature, summary, p_intensity, p_probability, 
        humidity, pressure, wspeed, wgust, wbearing, 
        cloudcover, uvindex, visibility)
        

    # SOMETHING WRONG HERE.... 
    def _enrich_parcel(self, parcel):
        flat_points = ','.join([str(s) for s in self.parcel_polygon_list])
        url = 'http://gis.richmondgov.com/ArcGIS/rest/services/StatePlane4502/Ener/MapServer/0/query?text=&geometry={}&inSR=&spatialRel=esriSpatialRelIntersects&relationParam=&objectIds=&where=&time=&returnCountOnly=false&returnIdsOnly=false&returnGeometry=true&maxAllowableOffset=&outSR=&outFields=&f=json'.format(flat_points)
        print('_enrich_parcel request url is: {}'.format(url))
        response = requests.get(url)
        print('_enrich_parcel response is: {}'.format(response.json()))

        # Since i'm not getting good data from the API... gonna fake this up.

        # Add the owners name
        parcel.parcel_owner_name = names.get_full_name()
        
        # Add mail address
        parcel.parcel_mail_address = '{} {} {}'.format(random.randrange(1, 300), names.get_first_name(), random.choice(['St.', 'Ave.', 'Blvd.', 'Way', 'Crossing', 'Rd', 'Pkwy']))
        
        # Add land value
        parcel.parcel_land_value = random.randrange(80000, 650000, 50) 
        
        # Add land sq ft
        parcel.parcel_land_sq_ft = random.randrange(600, 6500, 15) 
        
        # What else?   

    def _set_weather_lat_long(self):
        if 'address' in self.data and \
            'latitude' in self.data['address'] and \
            'longitude' in self.data['address']:

            self.weather_lat_long = [
                self.data['address']['latitude'], 
                self.data['address']['longitude'] 
            ]
        else:
            raise Exception('lat/long not found in address. Check file')
        
    def _set_parcel_polygon_list(self):
        '''
        To determine polygon for query:
            - incident address lat/long
            - for each unit's arrival lat/long

        Output: keep it simple, just a list of lat longs.
        (longitude first) -- so long/lats as specified in the API
        '''
        if self.weather_lat_long:
            # put in reverse order for api
            self.parcel_polygon_list.append(self.weather_lat_long[1])
            self.parcel_polygon_list.append(self.weather_lat_long[0])

        if 'apparatus' in self.data and len(self.data['apparatus']) > 2:
            # add to polygon
            apparatus = self.data['apparatus']
            for car in apparatus:
                if 'unit_status' in car and \
                        'arrived' in car['unit_status'] and \
                        'longitude' in car['unit_status']['arrived'] and \
                        'latitude' in car['unit_status']['arrived']:
                    self.parcel_polygon_list.append(car['unit_status']['arrived']['longitude'])
                    self.parcel_polygon_list.append(car['unit_status']['arrived']['latitude'])          
        else:
            raise Exception('Not enough data to create a polygon for parcel')


