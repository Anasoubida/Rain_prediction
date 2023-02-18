# -*- coding: utf-8 -*-
"""
Created on Tue Nov  1 19:00:41 2022

@author: Anas
"""
import requests ## to use the POST method we use a library named requests
## to send a new data to do predictions
data = {
  "dewptm": 2,
  "hum": 50,
  "month": 2,
  "pressurem": 400,
  "tempm": 20,
  "wspdm":30
}

# Change the localhost in case the api is running on another adress
url = 'http://localhost:8000/predict_body' ## this is the route we made for prediction
response = requests.post(url, json=data) ## post the customer information in json format
result = response.json() ## get the server response
print(result)


# to send a csv file as post request
file = open("data/test_api.csv", "rb")

payload = {
    "data": (file.name, file, "csv")
}

url = 'http://localhost:8000/predict_from_file' ## this is the route we made for prediction
response = requests.post(url, files=payload)

print(response.text)
