import yaml
import subscribe_to_farmbot.client as client
import subscribe_to_farmbot.my_device_id as my_device_id

class SequenceHander():
    def __init__(self,  yaml_file_name, csv_file_name):
        self.sequences = {}
        self.file = open(file_name, "r")

    def load_sequences(self, yaml_file_name, csv_file_name):
        """sequences : A dictionary of sequences, by "name or ID", to be stored as CeleryScript
           file_name : Name of the file the YAML sequence is stored in."""
        # Note: the "ID" is only obtained after sending it to FarmBot
        # So it will need to have a placeholder name until we get an ID for it
        file = open(file_name, "r")
        yaml_file = yaml.load(file)
        # Convert YAML to CeleryScript here
        for name in sequences:
            cs_obj = convert_sequence(yaml_file[name])
            client.publish("bot/" + my_device_id + "/from_clients", json_payload)

    def convert_sequence(yaml_obj):
        """yaml_obj: A YAML object representing a sequence
           returns: A CeleryScript JSON object of a sequence."""
           # This function can call itself to return well-formatted sub-sequences

    def example_sequence():
        """This is for the Regimen code writer to use. From a SequenceHander
        object it returns a dictionary with two named Sequences for them to use.
        The -if-then-else uses an existing sequence (ID: 2) loaded on the FarmBot"""
        return {"example" : """
        {
  "kind": "sequence",
  "name": "Example 1",
  "color": "gray",

  },
  "body": [
    {
      "kind": "_if",
      "args": {
        "lhs": "pin1",
        "op": "is",
        "rhs": 1,
        "_then": {
          "kind": "execute",
          "args": {
            "sequence_id": 2
          }
        },
        // Else branch
        "_else": {
          "kind": "nothing",
          "args": {
          }
        }
      }
    },
    {
      "kind": "wait",
      "args": {
        "milliseconds": 2300
      }
    }
  ]
}"""}
