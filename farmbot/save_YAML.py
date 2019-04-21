import yaml, json
import requests
import os

headers = {'Authorization': 'Bearer ' + os.getenv("API_KEY"), 'content-type': 'application/json'}
logs = requests.get('https://my.farmbot.io/api/logs', headers=headers)


file_handle=open('file.json',mode='w')
file_handle.write(logs.json())

file_read = open("file.json", 'r')
if file_read.mode == 'r':
    contents = file_read.read()
    contents = yaml.dump(json.load(contents))

file_handle2 = open("file.yaml", 'w+')
file_handle2.write(contents)
file_handle2.close()
