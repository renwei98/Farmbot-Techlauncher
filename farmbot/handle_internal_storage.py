import yaml, json
import requests
import os
import http_requests as http

print(type(os.getenv("API_KEY")))

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
    f = open(PATH, mode='r')
    file = yaml.load(f)
    name = "auto_"
    index = 1
    if file is not None:
        while True:
            if (name+str(index)) not in file:
                name = name+str(index)
                break
    else:
        f.close()
        return "auto_1"
    f.close()
    return name


def check_exist(name):
    f = open(PATH,mode='r')
    file = yaml.load(f)
    if file is None:
        f.close()
        return True, -1, -9
    elif name in file:
        f.close()
        return (True, file[key]["id"], file[name]["hash"])
    f.close()
    return False, -1, -9


def delete_all():
    f = open(PATH, mode='r+')
    file = yaml.load(f)
    if file is not None:
        for name in file:
            http.delete_command(file[name]["id"], file[name]["kind"])
            del file[name]
        yaml.dump(file, f)
        f.close()
    return


def delete_object(name):
    f = open(PATH, mode='r+')
    file = yaml.load(f)
    if file is None:
        return
    children = set()
    if "children" in file[name]:
        children = set(file[name]["children"])
    http.delete_command(file[name]["id"], file[name]["kind"])
    del file[name]
    yaml.dump(file, f)
    f.close()
    for child in children:
        delete_outdated(child)
    return


def delete_outdated(name):
    f = open(PATH, mode='r+')
    file = yaml.load(f)
    if file[name]["auto"]:
        children = set()
        if "children" in file[name]:
            children = set(file[name]["children"])
        http.delete_command(file[name]["id"], file[name]["kind"])
        del file[name]
        yaml.dump(file, f)
        f.close()
        for child in children:
            delete_outdated(child)
    return


def add_data(data):
    f = open(PATH, 'a')
    yaml.dump(data, f)
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
