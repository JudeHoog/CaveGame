import os
import requests
import json

lat = "40.6892"
lon = "-74.0445"

#dont steal my api key
response = requests.get("https://api.openweathermap.org/data/2.5/weather?lat="+lat+"&lon="+lon+"&appid=5362b9830508ec079bd2d89531909011&units=imperial")

#print(response.json())
print(response["coord"])
