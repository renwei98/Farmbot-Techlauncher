"""This class handles translating YAML into CeleryScript for both
   Sequences and Regimens."""

import yaml
import rw_internal_data as rw

class ActionHandler():
    def __init__(self,  yaml_file_names, csv_file_names):
        """yaml_file_names : a list of YAML files holding sequences and regimens
           csv_file_names  : a list of CSV files holding map coordinates"""
        self.source_files = {} # {source file : yaml object}
        self.seq_store = {} # {sequence name : internal YAML object}
        self.reg_store = {} # {regimen name : internal YAML object}
        self.evt_store = {} # {executable_id : internal YAML object}
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


    def to_datetime(date_string):

    def default_value(yaml_obj, field):
        if field == "every":
            if "every" in yaml:
                return yaml["every"]
            else:
                return str(1)
        elif field == "speed":

    def translate(yaml_obj, field):
        if field == "time_unit":
            if yaml["unit"] = "days":
                return "daily"
            else:
                return yaml["unit"][0:-1] + "ly"

    def make_and_send_sequence(list_obj):
        """list_obj : A list of actions that form a sequence.
           returns : The ID of the sequence sent, returned from FarmBot

           This function turns a list of actions into a YAML sequence with a
           program-set name, then turns it into a CeleryScript command, sends
           it off and gets the ID back, and writes the YAML sequence object
           with its name and ID to internal storage."""

    def make_and_send_regimen(schedule_yaml_obj, id=None):
        """schedule_yaml_obj : A yaml object that defines a schedule.
             schedule: [{days: [], times: [], actions: <<list of actions or name of sequence>>}
             OR
             schedule: [{every: 4, unit: "minutes/hours/days/weeks/months/years", actions: <<list of actions or name of sequence>>}
           returns : The ID of the sequence sent, returned from FarmBot

           This function turns a list of actions into a YAML sequence with a
           program-set name, then turns it into a CeleryScript command, sends
           it off and gets the ID back, and writes the YAML sequence object
           with its name and ID to internal storage."""

    def make_and_send_farm_event(list_obj):
        """list_obj : A list of actions that form a sequence.
           returns : The ID of the sequence sent, returned from FarmBot

           This function turns a list of actions into a YAML sequence with a
           program-set name, then turns it into a CeleryScript command, sends
           it off and gets the ID back, and writes the YAML sequence object
           with its name and ID to internal storage."""


    def convert_yaml(yaml_obj):
        """yaml_obj: A YAML object representing a sequence, regimen, or event
           returns: A CeleryScript JSON object of a sequence."""
           script = "{"
           # If the object is an event
           if "start_date" in yaml_obj:
               script  = script + "\n  \"start_time\" : \"" + yaml_obj["start_time"] + "\""
               if "repeat_event" in yaml_obj:
               # The following is a field in Farm Events:
               # repeat_event: {every: default 1, unit = "minutes/hours/days/weeks/months/years", until: ???}
                   script = script + "\n  \"end_time\" : \"" + to_datetime(yaml_obj["repeat_event"]["until"]) + "\""
                   script = script + "\n  \"repeat\" : " + default_value(yaml_obj["repeat_event"], "every") + "\""
                   script = script + "\n  \"time_unit\" : \"" + yaml_obj["repeat_event"]["unit"] + "\""
               else:
                   script = script + "\n  \"time_unit\" : " + "\"never\""
                   script = script + "\n  \"repeat\" : " + "\"1\""
               # This is a big, complicated if-else tree where the user might:
               #  - Put everything right here, and we have to create the sequences and regimens
               #  - Refer to a regimen
               #  - Refer to a sequence
               #  - Refer to a sequence but make it a regimen right here in this object
               #
               # If the user does not refer to another object
               if type(yaml_obj["action"]) is not str:
                   if "schedule" in yaml_obj:
                       script = script + "\n  \"executable_type\" : " + "\"regimen\""
                   else:
                       script = script + "\n  \"executable_type\" : " + "\"sequence\""
               elif rw.get_type(yaml_obj["action"]) == "regimen":
                   if "schedule" in yaml_obj:
                       print("The object referred to in Farm Event ") + yaml_obj["name"] + "is already a Regimen and does not need a schedule."
                       return
                   script = script + "\n  \"executable_type\" : " + "\"regimen\""

               # script = script + "\n  \"executable_id\" : \"" + rw.get_id(yaml_obj["action"]) + "\""/
               # script = script + "\n  \"executable_type\" : \"" + rw.get_type(yaml_obj["action"]) + "\""

    def add_seq_source(self, yaml_file):
        """Adds another YAML source file to the SequenceHandler."""
        self.source_files[yaml_file] = yaml.load(open(yaml_file, "r"))

    def add_map_source(self, csv_file):
        """Adds another map source file to the SequenceHandler."""
        self.map.add(csv_file)

    def delete_regimen(self, name):
        """Delete the regimen or inform the euser it has not been loaded."""

    def delete_sequence(self, name):
        """Delete the sequence or inform the euser it has not been loaded."""

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
