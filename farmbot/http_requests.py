import requests
from dotenv import load_dotenv
import os

load_dotenv()  # Add API_KEY to .env if not done already
headers = {'Authorization': 'Bearer ' + os.getenv("API_KEY"), 'content-type': 'application/json'}

# Get all sequences currently on Farmbot
sequences = requests.get('https://my.farmbot.io/api/sequences', headers=headers)
print(sequences.json())

# Create new example sequence
json = {
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

new_sequence = requests.post('https://my.farmbot.io/api/sequences', headers=headers, json=json)
sequence_id = new_sequence.json()['id']
print(new_sequence.json())
print("Sequence ID: ", sequence_id)

# Delete newly created example sequence
delete_sequence = requests.delete('https://my.farmbot.io/api/sequences/' + str(sequence_id), headers=headers)
print(delete_sequence, "Sequence:", sequence_id, "Deleted")
