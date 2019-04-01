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
        self.names = 0  # to assign unique names, will need to be replaced later
                        # when we start storing internal data

    def load_actions(self):
        """Modifies self.source_files, self.seq_script, and self.reg_script"""
        for source in self.source_files:
            yaml_file = yaml.load(open(source, "r"))
            self.source_files[source] = yaml_file

    def calc_time_offsets(days, times):
        """days : a list of days on which the sequence should be executed
           times : a list of days on which the sequence should be executed
           returns : a list of integers that are time_offset(s) for CeleryScript"""
        

    def to_datetime(date_string):

    def default_value(yaml_obj, field):
        if field == "every":
            if "every" in yaml_obj:
                return yaml_obj["every"]
            else:
                return str(1)
        elif field == "speed":
            if "speed" in yaml_obj:
                return yaml_obj["speed"]
            else:
                return str(50)
        elif field == "color":
            if "color" in yaml_obj:
                return yaml_obj["color"]
            else:
                return "gray"
    def translate(yaml_obj, field):
        if field == "time_unit":
            if yaml_obj["unit"] = "days":
                return "daily"
            else:
                return yaml_obj["unit"][0:-1] + "ly"

    def make_and_send_sequence(list_obj, name=None):
        """list_obj : A list of actions that form a sequence.
           name : If the sequence is user-defined rather than auto-generated, put its name here
           returns : The ID of the sequence sent, returned from FarmBot

           This function turns a list of actions into a YAML sequence with a
           program-set name, then turns it into a CeleryScript command, sends
           it off and gets the ID back, and writes the YAML sequence object
           with its name and ID to internal storage."""

    def make_and_send_regimen(regimen):
        """regimen : A yaml object that looks like this:
             schedule: [{days: [], times: [], actions: <<list of actions or name of sequence>>}
             OR
             schedule: [{every: 4, unit: "minutes/hours/days/weeks/months/years", actions: <<list of actions or name of sequence>>}
           name : If the regimen is user-defined rather than auto-generated, put its name here
           returns : The ID of the sequence sent, returned from FarmBot

           This function turns a list of actions into a YAML sequence with a
           program-set name, then turns it into a CeleryScript command, sends
           it off and gets the ID back, and writes the YAML sequence object
           with its name and ID to internal storage."""
        script = "{"
        script = script + "\n  \"color\": " + default_value(regimen, "color")
        if "name" in regimen:
            script = script + "\n  \"name\": " + regimen["name"]
        else:
            script = script + "\n  \"name\": " + "a_n_" + self.names
            self.names += 1
        list_of_sequences = [] # [(seq_id : , days : , times: [])]

        # Get IDs for all the sequences you need
        for sequence in regimen:
            sequence_id
            if type(actions) is not str:
                sequence_id = make_and_send_sequence(regimen["actions"])
            else:
                for file in self.source_files:
                    if yaml_obj["actions"] in file:
                        seq_obj = file[yaml_obj["actions"]]
                        if "schedule" in seq_obj:
                            print("Either they referred to a regimen as a sequence " +
                                "or implmented a sequence with regimen fields")
                        sequence_id = make_and_send_sequence(seq_obj)
                        break
            list_of_sequences.append({"id":sequence_id,"days":sequence["days"],
                "times":sequence["times"]})
        # Format all the sequences and their times for the regimen
        script = script + "\n  \"regimen_items\": [ \n    {"
        for sequence in list_of_sequences:
            for time in sequence["times"]:
                script = script + "\n      \"time_offset\": " + calc_time_offsets(regimen["days"], regimen["times"])
                script = script + "\n      \"sequence_id\": " + sequence[0]

    def make_and_send_farm_event(yaml_obj):
        """yaml_obj : An YAML object we already know is an event.
           returns : The ID of the event sent, returned from FarmBot

           This function turns a list of actions into a YAML event with a
           program-set name, then turns it into a CeleryScript command, sends
           it off and gets the ID back, and writes the YAML sequence object
           with its name and ID to internal storage."""
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
           # If the Farm Event requires you to make a Regimen
           if "schedule" in yaml_obj:
               regimen_id = make_and_send_regimen(yaml_obj["schedule"])
               script = script + "\n  \"executable_id\" : " + str(regimen_id)
               script = script + "\n  \"executable_type\" : " + "\"regimen\","
           else: # We don't need to extract a regimen from the event
               # No schedule and a list of actions can only mean "create a sequence"
               if type(yaml_obj["actions"]) is not str:
                   sequence_id = make_and_send_sequence(yaml_obj["actions"])
               # It refers to a regimen or sequence by name, we don't know which:
               else:
                   unknown_obj
                   for file in self.source_files:
                       if yaml_obj["actions"] in file:
                           unknown_obj = file[yaml_obj["actions"]]
                           break
                   # No schedule and no list of actions in the parent object
                   # But the child object is a Regimen
                   if "schedule" in unknown_obj:
                       if unknown_obj["actions"] is not str:
                           sequence_id = make_and_send_sequence(unknown_obj["actions"])
                           regimen_id = make_and_send_regimen(unknown_obj["schedule"], sequence_id)
                           script = script + "\n  \"executable_id\" : " + str(regimen_id)
                           script = script + "\n  \"executable_type\" : " + "\"regimen\","
                       else: # It refers to a sequence by name
                           regimen_id
                           for file in self.source_files:
                               if yaml_obj["actions"] in file:
                                   sequence_id = make_and_send_sequence(file[yaml_obj["actions"]])
                                   regimen_id = make_and_send_regimen(yaml_obj["schedule"], sequence_id)
                                   break
                           script = script + "\n  \"executable_id\" : " + str(regimen_id)
                           script = script + "\n  \"executable_type\" : " + "\"regimen\","
                   else: # Child object is a sequence
                       if unknown_obj["actions"] is not str:
                           sequence_id = make_and_send_sequence(unknown_obj["actions"])
                           script = script + "\n  \"executable_id\" : " + str(sequence_id)
                           script = script + "\n  \"executable_type\" : " + "\"sequence\","
                       else: # It refers to a sequence by name
                           sequence_id
                           for file in self.source_files:
                               if yaml_obj["actions"] in file:
                                   sequence_id = make_and_send_sequence(file[yaml_obj["actions"]])
                                   break
                           script = script + "\n  \"executable_id\" : " + str(sequence_id)
                           script = script + "\n  \"executable_type\" : " + "\"sequence\","

           elif rw.get_type(yaml_obj["actions"]) == "regimen":
               if "schedule" in yaml_obj:
                   return
               script = script + "\n  \"executable_type\" : " + "\"regimen\""


    def convert_yaml(yaml_obj):
        """yaml_obj: A YAML object representing a sequence, regimen, or event
           returns: A CeleryScript JSON object of a sequence."""
           script = "{"
           # If the object is an event
           if "start_date" in yaml_obj:
               make_and_send_farm_event(yaml_obj)

               # script = script + "\n  \"executable_id\" : \"" + rw.get_id(yaml_obj["actions"]) + "\""/
               # script = script + "\n  \"executable_type\" : \"" + rw.get_type(yaml_obj["actions"]) + "\""

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
