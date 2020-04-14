import requests

url = "https://whoisapi-whois-v2-v1.p.rapidapi.com/whoisserver/WhoisService"

querystring = {"outputFormat":"JSON","preferfresh":"0","da":"0","ip":"0","ipwhois":"0","checkproxydata":"0","thinWhois":"0","_parse":"0","domainName":"dusanpranj.com","apiKey":"at_QeXzUvthPOHCNZmAcA9z1u5LjQJ7B"}

headers = {
    'x-rapidapi-host': "whoisapi-whois-v2-v1.p.rapidapi.com",
    'x-rapidapi-key': "115bb7de32msh80ea723288170a8p1b9dd5jsn4ffcbc2ecb53"
    }

response = requests.request("GET", url, headers=headers, params=querystring)
response_final = response.json()
print(response_final["WhoisRecord"]["createdDate"])
print(response_final["WhoisRecord"]["createdDate"][:10])