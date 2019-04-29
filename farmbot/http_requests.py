import requests
from dotenv import load_dotenv
import os
from enum import Enum


class Event(Enum):
    REGIMEN = 'regimen'
    SEQUENCE = 'sequence'
    FARM_EVENT = 'farm_event'


load_dotenv()  # Add API_KEY to .env if not done already
headers = {'Authorization': 'Bearer ' + os.getenv("API_KEY"), 'content-type': 'application/json'}


# Get all sequences currently on Farmbot
def get_sequences():  # TODO be able to get regimens and farm events too
    sequences = requests.get('https://my.farmbot.io/api/sequences', headers=headers)
    return sequences.json()


def new_sequence(json_script, event_name: str, event_type: Event):  # TODO rename if sequence, regimen, event uses this
    id = -1

    if event_type == Event.FARM_EVENT:
        new_item = requests.post('https://my.farmbot.io/api/farm_events', headers=headers, json=json_script)
        id = new_item.json()["id"]
    elif event_type == Event.REGIMEN:
        new_item = requests.post('https://my.farmbot.io/api/regimens', headers=headers, json=json_script)
        id = new_item.json()["id"]
    elif event_type == Event.SEQUENCE:
        new_item = requests.post('https://my.farmbot.io/api/sequences', headers=headers, json=json_script)
        id = new_item.json()["id"]

    return id


def delete_command(id, kind):
    if kind == "farm_event":
        requests.delete('https://my.farmbot.io/api/farm_events/' + str(id), headers=headers)
    elif kind == "regimen":
        requests.delete('https://my.farmbot.io/api/regimens/' + str(id), headers=headers)
    elif kind == "sequence":
        requests.delete('https://my.farmbot.io/api/sequences/' + str(id), headers=headers)
