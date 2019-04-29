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

# if there is already an object with the same *NAME* in internal storage
#   return (True, id) so read_commands know not to re-send it but use the existing id instead
# else
#   return (False, -1)

# There should be a function that checks only (auto == True) objects
# and if no object depends on them, it deletes them both from FarmBot and internal storage.
# (see http_requests for the FarmBot functions you need)

# Internal storage format is:
# {"name":name, "auto":True/False, "kind":"regimen", "id":reg_id, "hash":6941904779894686356}

# And if auto==True, it will also have "parent":parent_name
# This field makes it easier to delete automatically generated objects when its
# user-generated parent object is deleted.

# "hash" is what we check against to see if the user has edited a YAML object and
# we need to re-send it.

# If the YAML object uses another user-defined YAML object, it will also have the field
# "child":[]
# This makes it easier to update all parent objects if a child object is changed by the user.

# Note: If the user wants to change a sequence, regimen, or farm event that has already
# been sent, we will have to delete the old one from FarmBot and update all objects
# that have it as a child, and update all "auto"==True objects that have it as its parent.




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