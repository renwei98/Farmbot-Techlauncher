"""This class handles translating YAML into CeleryScript for both
   Sequences and Regimens."""

import yaml

class ActionHandler():
    def __init__(self,  yaml_file_names, csv_file_names):
        """yaml_file_names : a list of YAML files holding sequences and regimens
           csv_file_names  : a list of CSV files holding map coordinates"""
        self.source_files = {} # {source file : yaml object}
        self.seq_script = {} # {sequence name : celeryscript}
        self.reg_script = {} # {regimen name : celeryscript}
        self.map = set(csv_file_names)
        self.load_actions()

    def load_actions(self):
        """Modifies self.source_files, self.seq_script, and self.reg_script"""
        for source in self.source_files:
            yaml_file = yaml.load(open(source, "r"))
            self.source_files[source] = yaml_file
            # DON'T convert YAML to CeleryScript here
            # Rachel: I'm going to change this so it gets done in
            # send_actions() instead.
            for node in yaml_file:
                if node["kind"]=="sequence":
                    if node["name"] not in self.sequences:
                        self.seq_script[node["name"]] = (convert_sequence(yaml_file[name]), source)
                    else:
                        print("Placeholder message for duplicate sequences")
                elif node["kind"]=="regimen":
                    if node["name"] not in self.sequences:
                        self.reg_script[node["name"]] = (convert_regimen(yaml_file[name]), source)
                    else:
                        print("Placeholder message for duplicate regimens")

    def convert_sequence(yaml_obj):
        """yaml_obj: A YAML object representing a sequence
           returns: A CeleryScript JSON object of a sequence."""
           # This function will need to refer to sub-sequences by name
           # and send them first until you get an id back
           # The send_actions() function should handle getting IDs


    def convert_regimen(yaml_obj):
        """yaml_obj: A YAML object representing a regimen
           returns: A CeleryScript JSON object of a regimen."""
           # This function will need to refer to sequences by name
           # and send them first until you get an id back
           # The send_actions() function should handle getting IDs

    # ** PATRICK TAKE NOTE **
    # Call this after sending a sequence, so we can store the returned ID
    def update_sequence(self, seq_name, returned_id):
        source_file = self.seq_script[seq_name][1]
        # Add the ID to the YAML object
        self.source_files[source_file][seq_name]["id"] = returned_id
        yaml.dump(self.source_files[source_file], source_file)

    def update_regimen(self, reg_name, returned_id):
        source = self.seq_script[seq_name][1]
        self.source_files[source][seq_name]["id"] = returned_id
        yaml.dump(self.source_files[source], source)

    def add_seq_source(self, yaml_file):
        """Adds another YAML source file to the SequenceHandler."""
        self.source_files[yaml_file] = yaml.load(open(yaml_file, "r"))

    def add_map_source(self, csv_file):
        """Adds another map source file to the SequenceHandler."""
        self.map.add(csv_file)

    def example_sequence():
        """This is for the Regimen code writer to use. From a SequenceHander
        object it returns a dictionary with two named Sequences for them to use.
        The -if-then-else uses an existing sequence (ID: 2) loaded on the FarmBot"""
        return {"Example 1" :
        """
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
