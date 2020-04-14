from flask import Flask, request
import requests
import json
import ncclient
from ncclient import manager
import xml.dom.minidom

############## Bot details ##############

bot_name = 'Incu_bot_2020@webex.bot'
#roomId = 'Y2lzY29zcGFyazovL3VzL1JPT00vMWM4ZWRjMjQtMzBmYi0zZTFjLTk3OTgtODU5ZGVlMTYyNThl'
token = 'YmJjNTc1YzAtODk1OC00MzRhLWI5MWItOGFmMTU2NzkwNjMyNzBkNmJmZTUtZWVl_PF84_consumer'
header = {"content-type": "application/json; charset=utf-8", 
		  "authorization": "Bearer " + token}


############## Nexus connectivity ##############

node = '127.0.0.1'

def connect(node):
    try:
    	device_connection = manager.connect(host = node, port = '2222', username = 'admin', password = 'Cisco!123', hostkey_verify = False, device_params={'name':'nexus'})
    	return device_connection
    except:
        print("Unable to connect " + node)
def getVersion(node):
    device_connection = connect(node)
    version = """
               <show xmlns="http://www.cisco.com/nxos:1.0">
                   <version>
                   </version>
               </show>
               """
    netconf_output = device_connection.get(('subtree', version))
    xml_doc = xml.dom.minidom.parseString(netconf_output.xml)
    version = xml_doc.getElementsByTagName("mod:nxos_ver_str")
    return "Version: "+str(version[0].firstChild.nodeValue)

def getHostname(node):
    device_connection = connect(node)
    hostname = """
               <show xmlns="http://www.cisco.com/nxos:1.0">
                   <hostname>
                   </hostname>
               </show>
               """
    netconf_output = device_connection.get(('subtree', hostname))
    xml_doc = xml.dom.minidom.parseString(netconf_output.xml)
    hostname = xml_doc.getElementsByTagName("mod:hostname")
    return "Hostname: "+str(hostname[0].firstChild.nodeValue)

def setHostname(node,name):
    device_connection = connect(node)
    update_hostname_config_string = """
	<configure xmlns="http://www.cisco.com/nxos:1.0">
        	<__XML__MODE__exec_configure>
            		<hostname><name>%s</name></hostname>
        	</__XML__MODE__exec_configure>
    </configure>
    """
    configuration = '<config>' + update_hostname_config_string % (name) + '</config>'
    device_connection.edit_config(target='running', config=configuration)
    return "Hostname changed to " + str(name)

def getWeather(city_name):
	base_url = "https://community-open-weather-map.p.rapidapi.com/weather"
	querystring = {"id": "2172797", "units": "%22metric%22 or %22imperial%22","mode": "xml%2C html", "q": city_name}
	headers = {
		'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com",
		'x-rapidapi-key': "115bb7de32msh80ea723288170a8p1b9dd5jsn4ffcbc2ecb53"
	}
	response = requests.request("GET", base_url, headers=headers, params=querystring)
	x = response.json()
	if x["cod"] != "404":
		y = x["main"]
		current_temperature = int(y["temp"]-273.15)
		current_presure = y["pressure"]
		current_humidity = y["humidity"]
		z = x["weather"]
		weather_decription = z[0]["description"]
		return " \n- Temperature (in celsius unit) = " + str(current_temperature) + " \n- atmospheric pressure (in hPa unit) = " + str(current_presure)  + " \n- humidity (in percentage) = " + str(current_humidity) + " \n- description = " + str(weather_decription)
	else:
		return "City Not Found"

def getCovid19(country_name):
	url = "https://covid-19-coronavirus-statistics.p.rapidapi.com/v1/stats"
	querystring = {"country": country_name}
	headers = {
		'x-rapidapi-host': "covid-19-coronavirus-statistics.p.rapidapi.com",
		'x-rapidapi-key': "115bb7de32msh80ea723288170a8p1b9dd5jsn4ffcbc2ecb53"
	}
	response = requests.request("GET", url, headers=headers, params=querystring)
	response_final = response.json()
	if response_final['message'].startswith('Country not found.'):
		return "Country Not Found"
	else:
		confirmed = response_final['data']['covid19Stats'][0]['confirmed']
		deaths = response_final['data']['covid19Stats'][0]['deaths']
		recovered = response_final['data']['covid19Stats'][0]['recovered']
	return "Statistic for " + str(country_name) + ": " + " \n- Confirmed = " + str(confirmed) + " \n- Deaths = " + str(deaths) + " \n- Recovered = " + str(recovered)

def getIPLocation(ip):
	url = "https://ip-geolocation-ipwhois-io.p.rapidapi.com/json/"
	querystring = {"ip": ip}
	headers = {
		'x-rapidapi-host': "ip-geolocation-ipwhois-io.p.rapidapi.com",
		'x-rapidapi-key': "115bb7de32msh80ea723288170a8p1b9dd5jsn4ffcbc2ecb53"
	}
	response = requests.request("GET", url, headers=headers, params=querystring)
	response_final = response.json()
	country = response_final["country"]
	city =response_final["city"]
	latitude = response_final["latitude"]
	longitude = response_final["longitude"]
	isp = response_final["isp"]

	if response_final["success"] == True:
		return "Information for " + str(ip) + ": " + " \n- Country = " + str(country) + " \n- City = " + str(city) + " \n- Latitude = " + str(latitude) + " \n- Longitude = " + str(longitude) + " \n- ISP = " + str(isp)
	else:
		return "Invalid IP address"

def getDomain(url_search):
	url = "https://whoisapi-whois-v2-v1.p.rapidapi.com/whoisserver/WhoisService"
	querystring = {"outputFormat": "JSON", "preferfresh": "0", "da": "0", "ip": "0", "ipwhois": "0", "checkproxydata": "0", "thinWhois": "0", "_parse": "0", "domainName": url_search, "apiKey": "at_QeXzUvthPOHCNZmAcA9z1u5LjQJ7B"}
	headers = {
		'x-rapidapi-host': "whoisapi-whois-v2-v1.p.rapidapi.com",
		'x-rapidapi-key': "115bb7de32msh80ea723288170a8p1b9dd5jsn4ffcbc2ecb53"
	}
	response = requests.request("GET", url, headers=headers, params=querystring)
	response_final = response.json()
	createdDate = response_final["WhoisRecord"]['createdDate'][:10]
	expiresDate = response_final["WhoisRecord"]['expiresDate'][:10]
	registrant = response_final["WhoisRecord"]['registrant']['name']
	city = response_final["WhoisRecord"]['registrant']['city']
	state = response_final["WhoisRecord"]['registrant']['state']
	return "Information for " + str(url_search) + ": " + " \n- Created date = " + str(createdDate) + " \n- Expires date = " + str(expiresDate) + " \n- Registrant = " + str(registrant) + " \n- City = " + str(city) + " \n- State = " + str(state)

############## Flask Application ##############

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def sendMessage():
	webhook = request.json
	url = 'https://api.ciscospark.com/v1/messages'
	msg = {"roomId": webhook["data"]["roomId"]}
	sender = webhook["data"]["personEmail"]
	message = getMessage()
	if (sender != bot_name):
		if (message == "help"):
			msg["markdown"] = "Welcome to **Cisco Nexus 9000 bot**!  \n List of available commands: \n- show version \n- show hostname \n- set hostname \n \n"
			msg["markdown"] += "Also, you can:  \n  \n- Check weather for any city with **Weather city_name** \n- Check number of COVID-19 for any country with **COVID19 country_name** \n- Get Information about IP address with **IP address_number** \n- Get Information about domain with **Domain domain_name**"
		elif (message.startswith('Weather')):
			city_name = message[7:]
			msg["markdown"] = str(getWeather(city_name))
		elif (message == "show version"):
			msg["markdown"] = getVersion(node)
		elif (message.startswith('hostname')):
			list = message.split(' ')
			msg["markdown"] = setHostname(node,list[1])
		elif (message == 'show hostname'):
			msg["markdown"] = getHostname(node)
		elif (message.startswith('COVID19')):
			msg["markdown"] = getCovid19(message[8:])
			print(message[8:])
		elif (message.startswith("IP")):
			msg["markdown"] = getIPLocation(message[3:])
		elif (message.startswith("Domain")):
			msg["markdown"] = getDomain(message[7:])
		else:
			msg["markdown"] = "Sorry! I didn't recognize that command. Type **help** to see the list of available commands."
		requests.post(url, data=json.dumps(msg), headers=header, verify=True)

def getMessage():
	webhook = request.json
	url = 'https://api.ciscospark.com/v1/messages/' + webhook["data"]["id"]
	get_msgs = requests.get(url, headers=header, verify=True)
	message = get_msgs.json()['text']
	return message

app.run()