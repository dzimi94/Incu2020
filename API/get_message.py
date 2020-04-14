import requests

roomId = 'Y2lzY29zcGFyazovL3VzL1JPT00vYWFhYzBjYjItM2UyYy0zMDg4LWJiODMtN2ZjODY4Mzg1YmUx'
token = 'YmJjNTc1YzAtODk1OC00MzRhLWI5MWItOGFmMTU2NzkwNjMyNzBkNmJmZTUtZWVl_PF84_consumer'

url = "https://api.ciscospark.com/v1/messages?roomId=" + roomId

header = {"content-type": "application/json; charset=utf-8", 
		  "authorization": "Bearer " + token}

response = requests.get(url, headers = header, verify = True)

print(response.json())