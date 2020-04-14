import requests

url = "https://ip-geolocation-ipwhois-io.p.rapidapi.com/json/"
querystring = {"ip":"37.19.109.163"}
headers = {
    'x-rapidapi-host': "ip-geolocation-ipwhois-io.p.rapidapi.com",
    'x-rapidapi-key': "115bb7de32msh80ea723288170a8p1b9dd5jsn4ffcbc2ecb53"
    }
response = requests.request("GET", url, headers=headers, params=querystring)
response_final = response.json()
print(response.text)
print(response_final['country'])