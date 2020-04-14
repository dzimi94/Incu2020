import requests

url = "https://covid-19-coronavirus-statistics.p.rapidapi.com/v1/stats"

querystring = {"country":"sdadsad"}

headers = {
    'x-rapidapi-host': "covid-19-coronavirus-statistics.p.rapidapi.com",
    'x-rapidapi-key': "115bb7de32msh80ea723288170a8p1b9dd5jsn4ffcbc2ecb53"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

response_final = response.json()
print(response.text)
print(str(response_final["data"]['covid19Stats'][0]['confirmed']))



