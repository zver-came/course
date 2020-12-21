import requests
import csv

url = "https://visual-crossing-weather.p.rapidapi.com/history"
querystring = {"startDateTime":"2010-03-01T00:00:00","aggregateHours":"6",
               "location":"Helsinki,FI","endDateTime":"2010-03-02T00:00:00",
               "unitGroup":"us","dayStartTime":"6:00:00","contentType":"csv",
               "dayEndTime":"18:00:00","shortColumnNames":"0"}
headers = {
    'x-rapidapi-key': "6a16679dd5msh83345a814e32133p1a61f1jsna0c3507d2e8b",
    'x-rapidapi-host': "visual-crossing-weather.p.rapidapi.com"
    }

def make_query_string(location,date_start,date_finish):
        querystring['startDateTime'] = date_start
        querystring['endDateTime'] = date_finish
        querystring['location'] = location

def upload_data():
    try:
        response = requests.get(url, headers=headers, params=querystring)
        return csv.DictReader(response.iter_lines(decode_unicode=True))
    except Exception as s:print(s)

