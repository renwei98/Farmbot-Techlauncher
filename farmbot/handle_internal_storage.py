import yaml, json
import requests
import os

headers = {'Authorization': 'Bearer ' + os.getenv("API_KEY"), 'content-type': 'application/json'}
logs = requests.get('https://my.farmbot.io/api/logs', headers=headers)

PATH = ".internal_storage/farmbot_commands.txt"

#Open a file named file.json or create one if it doesn't exist.
file_handle=open('file.json',mode='w')
file_handle.write(logs.json())

#Read file.json and transfer it to YAML.
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

# if there is already an object with the same *NAME* in internal storage
#   return (True, id, hash) so read_commands know not to re-send it but use the existing id instead
# else
#   return (False, -1, hash)

# There should be a function that checks only (auto == True) objects
# and if no object depends on them, it deletes them both from FarmBot and internal storage.
# (see http_requests for the FarmBot functions you need)

# Internal storage format is:
# {"name":name, "auto":True/False, "kind":"regimen", "id":reg_id, "hash":6941904779894686356}

# "hash" is what we check against to see if the user has edited a YAML object and
# we need to re-send it.

# "children":[]
# This makes it easier to update all parent objects if a child object is changed by the user.
# Automatically generated children *are* included here

# Note: If the user wants to change a sequence, regimen, or farm event that has already
# been sent, we will have to delete the old one from FarmBot and update all objects
# that have it as a child, and update all "auto"==True objects that have it as its parent.


def check_exist(name):
    file = yaml.load(open(PATH,mode='r'))
    for key in file:
        if obj == name:
            return (True, file[key]["id"])
    return (False, -1, file[name]["hash"])

def delete_object(name):
    file = yaml.load(open(PATH,mode='r'))
    children = set()
    if "children" in file[name]:
        children = set(file[name]["children"])
    del file[name]
    yaml.dump(file, open(PATH, 'w'))
    for child in children:
        delete_outdated(child)
    return

def delete_outdated(name):
    file = yaml.load(open(PATH,mode='r'))
    if file[name]["auto"]:
        children = set()
        if "children" in file[name]:
            children = set(file[name]["children"])
        del file[name]
        yaml.dump(file, open(PATH, 'w'))
        for child in children:
            delete_outdated(child)
    return

def add_data(data):
    yaml.dump(data, open(PATH, 'a'))
    return



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
