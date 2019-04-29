import yaml
from enum import Enum
import http_requests as http
from http_requests import Event


def sequence_to_celery(yaml_sequence):  # TODO maybe move to new file, this should convert yaml to celeryscript
    # Currently just sends example one, translation not implemented
    example_sequence = {
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
            }]
    }
    return example_sequence


file_contents = yaml.safe_load(open("../.internal_data/example.yaml"))
print(file_contents)

item_name = "my_sequence_name"
if item_name in file_contents:  # TODO cleanup section to be less messy
    if file_contents[item_name]['event_type'] == 'regimen':
        regimen_id = http.new_sequence(file_contents[item_name], item_name, Event.REGIMEN)

    elif file_contents[item_name]['event_type'] == 'sequence':
        sequence = sequence_to_celery(file_contents[item_name])
        sequence_id = http.new_sequence(file_contents[item_name], item_name, Event.SEQUENCE)
        print("Sequence ID: ", sequence_id)

    elif file_contents[item_name]['event_type'] == 'farm_event':
        event_id = http.new_sequence(file_contents[item_name], item_name, Event.FARM_EVENT)

    else:
        print("Invalid format for object")
