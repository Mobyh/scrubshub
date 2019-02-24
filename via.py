import re
import sys
import json
import requests
import datetime
import googlemaps

gmaps = googlemaps.Client(key='AIzaSyCUTg_2bQwxQZdOXQVeP43PQWe2fYeoqh4')

auth = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6Ii1zeE1KTUxDSURXTVRQdlp5SjZ0eC1DRHh3MCIsImtpZCI6Ii1zeE1KTUxDSURXTVRQdlp5SjZ0eC1DRHh3MCJ9.eyJhdWQiOiIyY2QyZmI5YS0xOGMyLTRlYjEtOTMxYi04ODg1YzYxNTE1NDgiLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC8yYTMwMzNjMi1hZDc2LTQyNmMtOWM1YS0yMzIzM2NkZTRjZGUvIiwiaWF0IjoxNTUwOTY1NTEyLCJuYmYiOjE1NTA5NjU1MTIsImV4cCI6MTU1MDk2OTQxMiwiYWlvIjoiNDJKZ1lBaGdDZEEzWTltVDY2SGhPa1Z3eitlVEFBPT0iLCJhcHBpZCI6IjQ2NmM4ZjM0LWUyYWYtNDJiYi04N2MyLTQ4MDIyMDYxNjhmNyIsImFwcGlkYWNyIjoiMSIsImlkcCI6Imh0dHBzOi8vc3RzLndpbmRvd3MubmV0LzJhMzAzM2MyLWFkNzYtNDI2Yy05YzVhLTIzMjMzY2RlNGNkZS8iLCJvaWQiOiIxZDVjYzM0Zi0zMWUwLTQ3ZTUtYTUxYy0wNDJkZjhiNDE3NzQiLCJzdWIiOiIxZDVjYzM0Zi0zMWUwLTQ3ZTUtYTUxYy0wNDJkZjhiNDE3NzQiLCJ0aWQiOiIyYTMwMzNjMi1hZDc2LTQyNmMtOWM1YS0yMzIzM2NkZTRjZGUiLCJ1dGkiOiJvZWFPcjRGNGNVYWdEZzNMenpCckFBIiwidmVyIjoiMS4wIn0.Il5qaa-mbz5dKkWBtc4VtPIPZt-SYtBbHt83Pz8xvcOOcKZPGFluMoEXzEaJzTuKLrkRuvOSEeOGGsqZ8V19iNLtuzY9M6KuPXWnsdBlmufevRqMzfj5vQ-rHlXzk0YBIdffGj85uHsrZ4VRiXq0mcBd18CKN5I--8-KG3-bGsBbnaMiP8I4vbhLkI-iDnXsC_1TOui7zggWVlbJoHZ3dEDNKF5Vk2VOOa3SEMGKL8mmpSgsNvOKOA1WKN45WiXG1co0F0Az0whA0C4yqwAPX82HVBt6wUI7t-IQScseFxlco6I9dRjN8202NtvSq8as0uZIXQjnE99AoncLNCxJNQ"

current = str(datetime.datetime.now().time())
times = [] #list of arrival times
stops = []
total = []
stop = 0
bus = 102 #Given by QR Code
p = re.compile("([0-9]{2}):([0-9]{2}):([0-9]{2})")

#Get info on bus
url = "https://codegtfsapi.viainfo.net/api/v1/bus-locations/" + str(bus)

payload = ""
headers = {
    'Authorization': auth,
    'cache-control': "no-cache",
    'Postman-Token': "3d211508-4cef-4155-9c76-36ae1f34df6e"
    }

response = requests.request("GET", url, data=payload, headers=headers)
data = json.loads(response.text)
trip = data['result']['tripId']
print(trip)

#Use bus info to get trip stop times
url = "https://codegtfsapi.viainfo.net/api/v1/stop-times/trip/" + str(trip)

payload = ""
headers = {
    'Authorization': auth,
    'cache-control': "no-cache",
    'Postman-Token': "6e62e0cc-e7d9-4523-9ee7-8b264f7cd85b"
    }

response = requests.request("GET", url, data=payload, headers=headers)
data = json.loads(response.text)

for x in data["result"]:
    times.append(x["arrivalTime"])
    stops.append(x["stopId"])

for x in times:
    m = re.match(p,x)
    hours = m.group(1)
    minutes = m.group(2)
    seconds = m.group(3)
    y = int(hours)*60*60 + int(minutes)*60 + int(seconds)
    total.append(y)
m = re.match(p,current)
dif = int(m.group(1))*60*60 + int(m.group(2))*60 + int(m.group(3))

if dif < total[0]:
    stop = stops[x]

for x in range(len(total)):
    if(dif < total[x] and x>0 and dif > total[x-1]):
        stop = stops[x]

if stop == 0:
    stop = stops[-1]

#Get coordinates of bus stop
url = "https://codegtfsapi.viainfo.net/api/v1/stops/" + str(stop)

payload = ""
headers = {
    'Authorization': auth,
    'cache-control': "no-cache",
    'Postman-Token': "4e05b2b5-40d5-4c61-b3df-c490d4ae001a"
    }

response = requests.request("GET", url, data=payload, headers=headers)
data = json.loads(response.text)

lat = data["result"]["latitude"]
lon = data["result"]["longitude"]

locations = gmaps.places('bar',str(lat)+','+str(lon),1000000)

for x in locations['results']:
    print(x['name'])




