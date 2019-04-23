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

stream = open('file.yml', 'r')
data = yaml.load(stream)
seq_ids=[]
reg_ids=[]
def check_seq_id(num):
    for k, v in data["YAML Sequence"].items():
         seq_ids.append(data["YAML Sequence"][k]["id"])
         if num in seq_ids:
             return True
         else:
             return False
         
def check_reg_id(num):
    for k, v in data["YAML Regimens"].items():
         reg_ids.append(data["YAML Regimens"][k]["id"])
         if num in reg_ids:
             return True
         else:
             return False
