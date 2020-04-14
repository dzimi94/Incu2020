import requests
import json

base_url = "https://community-open-weather-map.p.rapidapi.com/weather"
city_name = "Belgrade"
querystring = {"id": "2172797", "units": "%22metric%22 or %22imperial%22","mode": "xml%2C html", "q": city_name}
headers = {
	'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com",
	'x-rapidapi-key': "115bb7de32msh80ea723288170a8p1b9dd5jsn4ffcbc2ecb53"
}
response = requests.request("GET", base_url, headers=headers, params=querystring)
print("Temperatura je "+ str(int(response_final['main']['temp']-273.15)))



