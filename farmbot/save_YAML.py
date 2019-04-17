import yaml, json, sys
import requests
import os

headers = {'Authorization': 'Bearer ' + os.getenv("API_KEY"), 'content-type': 'application/json'}
logs = requests.get('https://my.farmbot.io/api/logs', headers=headers)


file_handle=open('file.json',mode='w')
file_handle.write(logs.json())

file_read = open("file.json", 'r')
if f.mode == 'r':
    contents = file_read.read()
    #contents = sys.stdout.write(yaml.dump(json.load(sys.stdin)))

file_handle = open("file.yaml", 'w+')
file_handle.write(contents)
file_handle.close()
