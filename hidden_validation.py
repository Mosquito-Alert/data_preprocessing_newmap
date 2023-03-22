# coding=utf-8
# !/usr/bin/env python
import requests
from requests.auth import HTTPBasicAuth
import json
from datetime import datetime
import config
import psycopg2
from django.utils.dateparse import parse_datetime

headers = {'Authorization': config.params['auth_token']}
years = [2014,2015,2016,2017,2018,2019,2020]

for year in years:
  r = requests.get("http://" + config.params['server_url'] + "/api/hidden_reports/?format=json" + "&year=" + str(year), headers=headers)
  if r.status_code == 200:
      file = "/tmp/hidden_reports_old" + str(year) + ".json"
      text_file = open(file, "w")
      text_file.write(r.text)
      text_file.close()
      print (str(year) + ' complete')    
  else:
      print ('Warning: report response status code for ' + str(year) + ' is ' + str(r.status_code))

  r = requests.get("http://" + config.params['server_url'] + "/api/hidden_reports_new/?format=json" + "&year=" + str(year), headers=headers)
  if r.status_code == 200:
      file = "/tmp/hidden_reports_new" + str(year) + ".json"
      text_file = open(file, "w")
      text_file.write(r.text)
      text_file.close()
      print (str(year) + ' complete')    
  else:
      print ('Warning: report response status code for ' + str(year) + ' is ' + str(r.status_code))

  json_data = open("/tmp/hidden_reports_new" + str(year) + ".json")
  data = json.load(json_data)
  ids_new = []
  for d in data:
    ids_new.append(d["version_UUID"])

  json_data = open("/tmp/hidden_reports_old" + str(year) + ".json")
  data = json.load(json_data)
  ids_old = []  
  for d in data:
    ids_old.append(d["version_UUID"])

  print("Checking equality " + str(year))
  print( set(ids_new) == set(ids_old) )
  
