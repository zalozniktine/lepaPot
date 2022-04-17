from math import sin, cos, sqrt, atan2, radians
import math
import sqlite3
import mysql.connector
import geopy.distance
import requests, json
from numpy import char
from numpy.core.defchararray import upper

api_key = "72c6bd207cc81e4fe9717a0a3d616548"
base_url = "http://api.openweathermap.org/data/2.5/weather?"

import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, LineString
#import plotly_express as px
import networkx as nx


#import pandas as pd

#df = pd.read_excel('worldcities.xlsx')
#df.head()

#from sqlalchemy import create_engine
# format: mysql://user:pass@host/db
#engine = create_engine('mysql://admin:admin@localhost/worldcities')
#df.to_sql('city', con=engine)

import mysql.connector
import pandas as pd

city = []
city_latitude = []
city_longitude = []

mydb = mysql.connector.connect(
  host="localhost",
  user="admin",
  password="admin",
  database="worldcities"
)
mycursor = mydb.cursor()
startingCity = (input("Enter your starting city: "))
startingCity = startingCity.upper()
endingCity = (input("Enter your destination city: "))
endingCity = endingCity.upper()

#get coordinates of starting city from database
mycursor.execute("SELECT * FROM city WHERE UPPER(city) = '" + startingCity + "'")

mesta = mycursor.fetchall()
for row in mesta:
    print("To je mesto zacetek: ", row[1])
    latitude = row[3]
    longitude = row[4]
    #convert string to float
    latitude = float(latitude)
    longitude = float(longitude)


mycursor.execute("SELECT * FROM city WHERE UPPER(city) = '" + endingCity + "'")

mesta = mycursor.fetchall()
for row in mesta:
    print("To je mesto konec: ", row[1])
    final_latitude = row[3]
    final_longitude = row[4]
    
    final_latitude = float(final_latitude)
    final_longitude = float(final_longitude)




test = ''
#latitude = 45.920500
#longitude = 14.509161
#coords_1 = (46.046082, 14.490898)


#final_latitude = 39.347962
#final_longitude = 22.424239

la = latitude - final_latitude
lo = longitude - final_longitude

if (la>0):
    final_latitude = final_latitude - 0.5
else:
    final_latitude = final_latitude + 0.5

if (lo > 0):
    final_longitude = final_longitude - 2
else:
    final_longitude = final_longitude + 2


city_cords = str(latitude) + ', ' + str(longitude)
end_cords = str(final_latitude) + ', ' + str(final_longitude)

while(geopy.distance.distance(city_cords, end_cords).km > 300 and test != city):
    mycursor.execute("SELECT city, lat, lng FROM city WHERE (((((acos(sin(( %s *pi()/180)) * sin((lat*pi()/180)) + cos(( %s *pi()/180)) * cos((lat*pi()/180)) * cos((( %s - lng) * pi()/180)))) * 180/pi()) * 60 * 1.1515 * 1.609344) <= 150) AND ((((acos(sin(( %s *pi()/180)) * sin((lat*pi()/180)) + cos(( %s *pi()/180)) * cos((lat*pi()/180)) * cos((( %s - lng) * pi()/180)))) * 180/pi()) * 60 * 1.1515 * 1.609344) > 100))", (latitude, latitude, longitude, latitude, latitude, longitude))

    print('Current latitude:'+str(latitude)+' Current longitude: '+str(longitude))

    myresult = mycursor.fetchall()
    test = city
    for row in myresult:
        city = row[0]
        city_latitude = row[1]
        city_longitude = row[2]
        city_cords = str(city_latitude) + ', ' + str(city_longitude)

        #print(str(test)+str(city))
        #if((test == city) or ((la>0) and city_latitude > latitude ))or((la<0 and city_latitude < latitude ))or((lo>0 and city_longitude > longitude ))or((lo<0 and city_longitude < longitude )):
        if (test == city) or ((la > 0) and city_latitude > (latitude)) or ((la > 0) and city_latitude < (final_latitude)) or ((la < 0) and city_latitude > (final_latitude)) or ((la < 0) and city_latitude < (latitude))or((lo > 0) and city_longitude > (longitude))or((lo > 0) and city_longitude < (final_longitude))or((lo < 0) and city_longitude > (final_longitude))or((lo < 0) and city_longitude < (longitude)):
            continue
        else:

            complete_url = base_url + "appid=" + api_key + "&q=" + city
            response = requests.get(complete_url)
            x = response.json()
            if x["cod"] != "404":
                y = x["main"]
                z = x["weather"]
                weather_description = z[0]["main"]
                if(weather_description == 'Clear'):
                    latitude = city_latitude
                    longitude = city_longitude
                    print(city)
                    break
                elif(weather_description == 'Clouds'):
                    latitude = city_latitude
                    longitude = city_longitude
                    print(city)
                    break
                elif (weather_description == 'Drizzle'):
                    latitude = city_latitude
                    longitude = city_longitude
                    print(city)
                    break
                elif (weather_description == 'Rain'):
                    latitude = city_latitude
                    longitude = city_longitude
                    print(city)
                    break
                elif (weather_description == 'Thunderstorm'):
                    latitude = city_latitude
                    longitude = city_longitude
                    print(city)
                    break
                elif (weather_description == 'Snow'):
                    latitude = city_latitude
                    longitude = city_longitude
                    print(city)
                    break
                elif (weather_description == 'Atmosphere'):
                    latitude = city_latitude
                    longitude = city_longitude
                    print(city)
                    break




