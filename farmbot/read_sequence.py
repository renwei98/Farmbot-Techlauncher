import yaml
import subscribe_to_farmbot.client as client
import subscribe_to_farmbot.my_device_id as my_device_id

class SequenceHander():
    def __init__(self,  yaml_file_names, csv_file_names):
        """yaml_file_names : a list of YAML files holding sequences
           csv_file_names  : a list of CSV files holding map coordinates"""
        self.seq_files = {} # {source file : yaml object}
        self.celeryscript = {} # {sequence name : celeryscript}
        self.seq_files = set(yaml_file_names)
        self.map = set(csv_file_names)
        self.load_sequences()

    def load_sequences(self):
        """Modifies self.seq_files and self.celeryscript"""
        for source in self.seq_files:
            file = open(source, "r")
            yaml_file = yaml.load(file)
            self.seq_files[source] = yaml_file
            # Convert YAML to CeleryScript here
            for node in yaml_file:
                if node["kind"]=="sequence":
                    if node["name"] not in self.sequences:
                        self.celeryscript[node["name"]] = (convert_sequence(yaml_file[name]), source)
                    else:
                        print("Placeholder message for duplicate sequences")

    def convert_sequence(yaml_obj):
        """yaml_obj: A YAML object representing a sequence
           returns: A CeleryScript JSON object of a sequence."""
           # This function will need to refer to sub-sequences by name
           # and send them first until you get an id back

    # ** PATRICK TAKE NOTE **
    # Call this after sending a sequence, so we can store the returned ID
    def update_sequence(self, seq_name, returned_id):
        source = self.celeryscript[seq_name][1]
        self.seq_files[source][seq_name]["id"] = returned_id
        yaml.dump(self.seq_files[source], source)

    def add_seq_source(self, yaml_file):
        """Adds another YAML source file to the SequenceHandler."""
        self.seq_files.add(yaml_file)

    def add_map_source(self, csv_file):
        """Adds another map source file to the SequenceHandler."""
        self.map.add(csv_file)

    def example_sequence():
        """This is for the Regimen code writer to use. From a SequenceHander
        object it returns a dictionary with two named Sequences for them to use.
        The -if-then-else uses an existing sequence (ID: 2) loaded on the FarmBot"""
        return {"Example 1" : """
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
