import requests
from dotenv import load_dotenv
import os
from enum import Enum


class Event(Enum):
    REGIMEN = 'regimen'
    SEQUENCE = 'sequence'
    FARM_EVENT = 'farm_event'

example_script = """{
  "name": "EXAMPLE SEQUENCE",
  "body": [
    {
      "kind": "move_absolute",
      "args": {
        "location": {
          "kind": "coordinate",
          "args": {
            "x": 1,
            "y": 2,
            "z": 3
          }
        },
        "offset": {
          "kind": "coordinate",
          "args": {
            "x": 0,
            "y": 0,
            "z": 0
          }
        },
        "speed": 4
      }
    }
  ]
}"""

load_dotenv()  # Add API_KEY to .env if not done already
headers = {'Authorization': 'Bearer ' + os.getenv("API_KEY"), 'content-type': 'application/json'}


# Get all sequences currently on Farmbot
def get_sequences():  # TODO be able to get regimens and farm events too
    sequences = requests.get('https://my.farmbot.io/api/sequences', headers=headers)
    return sequences.json()


def get_events():
    events = requests.get('https://my.farmbot.io/api/farm_events', headers=headers)
    return events.json()


# Sends CeleryScript objects to FarmBot and returns the ID.
def new_command(json_script, event_type: str):  # TODO rename if sequence, regimen, event uses this
    id = -1
    if event_type == "farm_event":
        new_item = requests.post('https://my.farmbot.io/api/farm_events', headers=headers, json=json_script)
        id = new_item.json()["id"]
    elif event_type == "regimen":
        new_item = requests.post('https://my.farmbot.io/api/regimens', headers=headers, json=json_script)
        id = new_item.json()["id"]
    elif event_type == "sequence":
        new_item = requests.post('https://my.farmbot.io/api/sequences', headers=headers, json=json_script)
        print("\n",new_item.json(),"\n")
        id = new_item.json()["id"]
    return id


# Tells FarmBot to delete something
def delete_command(id, kind):
    if kind == "farm_event":
        requests.delete('https://my.farmbot.io/api/farm_events/' + str(id), headers=headers)
    elif kind == "regimen":
        requests.delete('https://my.farmbot.io/api/regimens/' + str(id), headers=headers)
    elif kind == "sequence":
        requests.delete('https://my.farmbot.io/api/sequences/' + str(id), headers=headers)
