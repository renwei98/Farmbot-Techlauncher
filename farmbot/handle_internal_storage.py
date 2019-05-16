import yaml, json
import requests
import os
import http_requests as http



headers = {'Authorization': 'Bearer ' + os.getenv("API_KEY"), 'content-type': 'application/json'}
logs = requests.get('https://my.farmbot.io/api/logs', headers=headers)

PATH = "../.internal_data/farmbot_commands.yaml"


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

def unique_name():
    f = open(PATH,mode='r+')
    file = yaml.load(f)
    name = "auto_"
    # return name
    index = 1
    if file is not None:
        while True:
            if (name+str(index)) not in file:
                name = name+str(index)
                break
            index += 1
    else:
        file = {name : {}}
        yaml.dump(file, f)
        f.close()
        return name
    if file is not None:
        file[name] = {}
    else:
        file = {name : {}}
    yaml.dump(file, f)
    f.close()
    return name

def check_exist(name, map):
    """returns
       (does it exist, ID, hash of command, hash of csv, list of its children) """
    f = open(PATH,mode='r')
    file = yaml.load(f)
    f.close()
    if file is None:
        return (False, -1, -9, -9, [])
    elif name in file:
        if "CSV" in file[name]:
            return (True, file[name]["id"], file[name]["hash"], file[name]["csv_hash"], file[name]["children"])
        else:
            return (True, file[name]["id"], file[name]["hash"], -9, file[name]["children"])
    elif name+"_"+map in file:
        n = name+"_"+map
        if "CSV" in file[n]:
            return (True, file[n]["id"], file[n]["hash"], file[n]["csv_hash"], file[n]["children"])
        else:
            return (True, file[n]["id"], file[n]["hash"], -9, file[n]["children"])
    return (False, -1, -9, -9, [])

def check_need_csv(name):
    f = open(PATH,mode='r')
    file = yaml.load(f)
    f.close()
    if "CSV" in file[name]:
        return (True, file[name]["csv_hash"])
    else:
        return (False, -1)

def delete_all():
    f = open(PATH,mode='r')
    file = yaml.load(f)
    f.close()
    if file is not None:
        for kind in ["farm_event","regimen","sequence"]:
            for name in list(file.keys()):
                if name in file and file[name]['kind'] == kind:
                    http.delete_command(file[name]["id"], file[name]["kind"])
                    del file[name]
        f = open(PATH,mode='w')
        f.write("")
        f.close()
    return

def delete_object(name):
    f = open(PATH,mode='r')
    file = yaml.load(f)
    f.close()
    if file is None:
        return
    children = []
    if "children" in file[name]:
        children = file[name]["children"]
    http.delete_command(file[name]["id"], file[name]["kind"])
    del file[name]
    if len(file.keys())!=0:
        f = open(PATH,mode='w')
        yaml.dump(file, f)
        f.close()
    else:
        f = open(PATH,mode='w')
        f.write('')
        f.close()
        return
    for child in children:
        if file[child]["auto"]:
            delete_outdated(child)
    return

def delete_outdated(name):
    f = open(PATH,mode='r')
    file = yaml.load(f)
    f.close()
    children = []
    if "children" in file[name]:
        children = file[name]["children"]
    http.delete_command(file[name]["id"], file[name]["kind"])
    del file[name]
    if len(file.keys())!=0:
        f = open(PATH,mode='w')
        yaml.dump(file, f)
        f.close()
    else:
        f = open(PATH,mode='w')
        f.write('')
        f.close()
        return
    for child in children:
        if file[child]["auto"]:
            delete_outdated(child)
    return

def add_data(data):
    name = list(data.keys())[0]
    f = open(PATH, 'r+')
    file = yaml.load(f)
    file[name] = data[name]
    yaml.dump(file, f)
    f.close()
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
