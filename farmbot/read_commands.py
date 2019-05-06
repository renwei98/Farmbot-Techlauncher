"""This class handles translating YAML into CeleryScript for both
   Sequences and Regimens."""

import yaml
import csv

import json
import http_requests as http
import datetime
from time import timezone
import handle_internal_storage as stor
# import

# device_id = api_token_gen.token_data['token']['unencoded']['bot']
# mqtt_host = api_token_gen.token_data['token']['unencoded']['mqtt']
# token = api_token_gen.token_data['token']['encoded']

class ActionHandler():
    PATH = ".internal_storage/farmbot_commands.txt"
    def __init__(self, yaml_file_names, default_settings=None, csv_file_name=None):
        """yaml_file_names  : YAML files
           default_settings : a single file containing
           csv_file_names   : a list of CSV files holding map coordinates"""
        self.source_files = {} # {file : {pin_aliases : {alias : PIN}}}
        self.map = csv_file_name
        self.settings = (1, 50, 0, 0, 0, 0) #scale, speed, z, x_offset, y_offset, z_offset
        # self.get_defaults(yaml_file_names, default_settings)
        # self.load_actions()

    def get_defaults(self, yaml_file_names, default_settings):
        if type(default_settings) is not None:
            settings = yaml.load(open(default_settings, 'r'))
            if "scale" in settings:
                self.settings = settings["scale"]
            if "default_speed" in settings:
                self.settings = settings["default_speed"]
            if "default_z" in settings:
                self.settings = settings["default_z"]
            if "default_x_offset" in settings:
                self.settings = settings["default_x_offset"]
            if "default_y_offset" in settings:
                self.settings = settings["default_y_offset"]
            if "default_z_offset" in settings:
                self.settings = settings["default_z_offset"]
        sources = set(yaml_file_names)
        for file_name in sources:
            file = yaml.load(open(f, 'r'))
            self.source_files[f] = {}
            if "options" in file:
                if "pin_aliases" in file["options"]:
                    for alias in file["options"]["pin_aliases"]:
                        self.source_files[file_name]["pin_aliases"][alias] = file[alias]
            if "other_files" in file["options"]: # aka it refers to other files
                    sources.union(set(file[key]))

    def obj_from_name(self, name):
        """name : the name of a YAML object
           returns : the ID of the sent object, and its type

           This function figues out if a name refers to a regimen or a sequence,
           calls the right function, and give returns the ID."""
        for file_name in self.source_files:
            file = yaml.load(open(file_name))
            if name in file:
                if "schedule" in file[name]:
                    id, name = self.make_regimen(file[name], file_name, name)
                    return (id, "regimen", name)
                elif "actions" in file[name]:
                    if file[name["actions"]] is not str:
                        id, name = self.make_sequence(file[name], file_name, name)
                        return (id, "sequence", name)
                    else:
                        return self.obj_from_name(file[name["actions"]])
                else:
                    print("Invalid format for object", name)

    def load_commands(self):
        """Modifies self.source_files, self.seq_script, and self.reg_script
           corrosponds to 'process_a_file' in the pseudocode"""
        file = yaml.load(open(yaml_file_name))
        if "other_files" in file:
            self.source_files.union(set(file["other_files"]))
        for source in self.source_files:
            file = yaml.load(open(source, "r"))
            self.source_files[source] = yaml_file
            for name in file:
                if "start_time" in yaml_obj:
                    self.make_farm_event(file[name], name, source)
                elif "schedule" in yaml_obj:
                    self.make_regimen(file[name], name, source)
                elif "actions" in yaml_obj:
                    self.make_sequence(file[name], name, source)
                else:
                    print("Invalid format for object:", name, source)

    def calc_time_offsets(self, schedule):
        """regimen : A yaml object that includes this:
           schedule: [{group: [optional], type: [optional], days: [], times: [], actions: <<list of actions or name of sequence>>}
           OR
           schedule: [{group: [optional], type: [optional], every: 4, unit: "minutes/hours/days/weeks/months/years", max: 10, actions: <<list of actions or name of sequence>>}
           returns : a list of integers that are time_offset(s) for CeleryScript"""
        time_offsets = []
        if "days" in schedule:
            days = schedule["days"]
            times = []
            for time in schedule["times"]:
                times.add(int(time[0:2])*60*60*1000 + int(time[3:])*60*1000)
            now = datetime.datetime.now()
            for day in days:
                begin = (day - 1) * 24*60*60*1000
                for time in times:
                    time_offsets.add(begin+time)
        elif "every" in schedule:
            every = schedule["every"]
            unit = schedule["unit"]
            period = 0
            if unit == "minutes":
                period = every*60*1000
            elif unit == "hours":
                period = every*60*60*1000
            elif unit == "days":
                period = every*24*60*60*1000
            elif unit == "weeks":
                period = every*7*24*60*60*1000
            elif unit == "months":
                period = every*30*24*60*60*1000
            elif unit == "years":
                period = every*365*24*60*60*1000
            for i in range(0,max):
                time_offsets.add(i*period)
            return time_offsets

    def format_time(self, time):
        """time: DD/MM/YYYY 23:00
           returns: YYYY-MM-DDT23:00:00.000Z aka ISO 8601 date representation, local time."""
        string = time[6:10]+"-"+time[3:5]+"-"+time[0:2]+"T"+time[11:]+":00"
        tz = int(timezone / 3600.0)
        if (tz < 0):
            return string + str(tz) + ":00"
        else:
            return string + "+" + str(tz) + ":00"

    def default(self, yaml_obj, field):
        if field == "color":
            if "color" in yaml_obj:
                return yaml_obj["color"]
            else:
                return "gray"
        elif field == "every":
            if "every" in yaml_obj:
                return yaml_obj["every"]
            else:
                return str(1)
        elif field == "speed":
            if "speed" in yaml_obj:
                return yaml_obj["speed"]
            else:
                return str(self.settings[1])
        elif field == "z":
            if "z" in yaml_obj:
                return yaml_obj["z"]
            else:
                return str(self.settings[2])
        elif field == "x_off":
            if "x_offset" in yaml_obj:
                return yaml_obj["x_offset"]
            else:
                return str(self.settings[3])
        elif field == "x_off":
            if "x_offset" in yaml_obj:
                return yaml_obj["x_offset"]
            else:
                return str(self.settings[4])
        elif field == "x_off":
            if "x_offset" in yaml_obj:
                return yaml_obj["x_offset"]
            else:
                return str(self.settings[5])

    def translate(self, yaml_obj, field):
        if field == "time_unit":
            if yaml_obj["unit"] == "days":
                return "daily"
            else:
                return yaml_obj["unit"][0:-1] + "ly"

    def pin_name(self, pin, source):
        if pin in self.source_files[source]["pin_aliases"]:
            return self.source_files[source]["pin_aliases"][pin]
        else:
            return pin

    def parse_coord(self, x=0,y=0,z=0,row=None):
        if row == None:
            return "{\"kind\": \"coordinate\",\"args\": {\"x\": "+ x + "\"y\": " + y + "\"z\": " + z + "} },"
        else:
            script = "{\"kind\": \"coordinate\",\"args\": {\"x\": "+ row["x"] + "\"y\": " + row["y"] + "\"z\": "
            if row["z"].strip()!="":
                script = script + row["z"] + "} },"
            else:
                script = script + default({},"z") + "} },"
            return script

    def parse_action(self,action, source_file, row=None):
        script = ""
        if "move_abs" in action:
            args = action["move_abs"]
            script = script + "{\"kind\":\"move_absolute\","
            script = script + "\"args\": {\"location\": " + parse_coord(args["x"], args["y"], self.default(args,"z"))
            script = script + "\"args\": {\"offset\": " + parse_coord(self.default(args,"x_off"), self.default(args,"y_off"), self.default(args,"z_off"))
            script = script + "\"speed\": " + self.default(args, "speed") + "},},"
        elif "move_rel" in action:
            args = action["move_rel"]
            script = script + "{\"kind\":\"move_relative\","
            script = script + "\"args\": {\"location\": " + parse_coord(args["x"], args["y"], self.default(args,"z"))
            script = script + "\"speed\": " + self.default(args, "speed") + "},},"
        elif "find_home" in action:
            script = script + "{\"kind\":\"find_home\",{\"args\": { \"axis\": "
            args = action["find_home"]
            if "x" in args:
                script = script + "\"x\","
            if "y" in args:
                script = script + "\"y\","
            if "z" in args:
                script = script + "\"z\","
            else:
                script = script + "\"all\","
            script = script + "\"speed\": " + self.default(args, "speed") + "},},"
        elif "wait" in action:
            return "{\"kind\": \"wait\", \"args\": { \"milliseconds\": \""+ action["wait"] + "\" } },"
        elif "read_pin" in action:
            args = action["read_pin"]
            script = script + "{\"kind\": \"read_pin\", \"args\": { "
            if "label" in args["read_pin"]:
                script = script + "\"label\": \""+ args["label"] +"\","
            script = script + "\"pin_number\": \""+ self.pin_name(args["pin"], source_file) +"\", \"pin_mode\": \""+ args["mode"] + "\" } },"
        elif "write_pin" in action:
            args = action["write_pin"]
            script = script + "{\"kind\": \"write_pin\", \"args\": { "
            script = script + "\"pin_mode\": \""+ args["mode"] +"\","
            script = script + "\"pin_number\": \""+ self.pin_name(args["pin"], source_file) +"\"," "\"pin_value\": \""+ action["value"] ++ "\" } },"
            # Note, I'm not sure if the pin_value for Digital mode can be a string or if it must be an integer
        elif "to_self" in action:
            script = script + "{\"kind\":\"move_absolute\","
            script = script + "\"args\": {\"location\": " + self.parse_coord(row=row)
            script = script + "\"args\": {\"offset\": " + self.parse_coord(self.default(action,"x_off"), self.default(action,"y_off"), self.default(action,"z_off"))
            script = script + "\"speed\": " + self.default(action, "speed") + "},},"
        elif "to_plant" in action:
            with open(self.map, "r") as csv_file:
                reader = csv.Dictreader(csv_file)
                for row in reader:
                    if row["name"].strip() == action["to_plant"]:
                        script = script + "{\"kind\":\"move_absolute\","
                        script = script + "\"args\": {\"location\": " + self.parse_coord(row=row)
                        script = script + "\"args\": {\"offset\": " + self.parse_coord(self.default(action,"x_off"), self.default(action,"y_off"), self.default(action,"z_off"))
                        script = script + "\"speed\": " + self.default(action, "speed") + "},},"
        elif "if" in action:
            script = script + "{\"kind\":\"_if\","
            script = script + "\"args\": {\"lhs\": "+ self.pin_name(args["pin"])+"\"," "\"op\": \""+ operator +"\"," "\"rhs\": \""+ action["value"] +"\","
            script = script + "\"_then\": { "
            if parse_operator(operator)(self.pin_name(args["pin"]), action["value"]):
                script = script + "{\"kind\":\"execute","
                script = script + "\"args\": {\"sequence_id\": " + self.default(action, "sequence_id") +"\","" + " } },"
                script = script + "\"_else\": { "
                script = script + "{\"kind\":\"nothing","
                script = script + "\"args\": { " + "\","" + " } } } }"
            else:
                script = script + "{\"kind\":\"nothing","
                script = script + "\"args\": { " +"\","" + " } },"
                script = script + "\"_else\": { "
                script = script + "{\"kind\":\"execute","
                script = script + "\"args\": {\"sequence_id\": " + self.default(action, "sequence_id") +"\","" + " } },"
                
        else:
            raise Error("The action " + action.keys()[0] + " is undefined.")
        return script
    
    import operator
    def parse_operator(string):
        """get the operator from the string given"""
        ops = {
                "is": operator.is_,
                "is not": operator.is_not,          
                }
        return ops[string]

    def check_change(self, yaml_obj, name):
        """Checks if an object or any object it depends on has changed.
           IF an object has been changed, it automatically deletes that object from storage.
           yaml_obj: the new obejct definition
           name: the name of the object
           hash: the new hash of the object"""
        existance, id, stored_hash = stor.check_exist(name)
        if existance:
            if stored_hash == hash(json.dumps(yaml_obj)):
                # If the actions include user-defined objects, check if they changed.
                for child in yaml_obj["actions"]:
                    if type(child) is str:
                        for name in self.source_files:
                            file = yaml.load(open(name, mode='r'))
                            if child in file:
                                if self.check_change(file[name], child):
                                    stor.delete_object(name)
                                    return (True, id)
                return (False, id)
            else: # Already exists in storage and has changed
                stor.delete_object(name)
                return (True, id)
        else:
            return (False, id)

    def make_sequence(self, yaml_obj, source_file, name = None):
        """sequence : Includes or is a list of actions.
           returns : The ID of the sequence sent, returned from FarmBot

           This function turns a list of actions into a YAML sequence with a
           program-set name, then turns it into a CeleryScript command, sends
           it off and gets the ID back, and writes the YAML sequence object
           with its name and ID to internal storage."""
        if type(name) is not None:
            changed, id = self.check_change(yaml_obj, name)
            if not changed:
                return (id, name)

        script = "{"
        name = ""
        auto = 1 # not-zero is true
        seq_id = -1
        if "name" in yaml_obj:
            name = yaml_obj["name"]
            auto = 0 # zero is false
        else:
            name = stor.unique_name()
        script = script + "\n  \"name\": " + name + ","
        data = {"name" : name, "auto": auto, "kind" : "regimen", "hash":hash(json.dumps(yaml_obj)), "children":[]}

        script = script + "\n  \"body\": [ \n    {"
        actions = yaml_obj["actions"]
        if actions is not str:
            with open(self.map, "r") as csv_file:
                reader = csv.Dictreader(csv_file)
                if "group" in yaml_obj and "type" in yaml_obj:
                    groups = yaml_obj["groups"]
                    types = yaml_obj["types"]
                    for row in reader:
                        if row["group"].strip() in groups or row["types"].strip() in types:
                            for action in actions:
                                if "to_self" in action:
                                    script = script + self.parse_action(action, source_file, row)
                                else:
                                    script = script + self.parse_action(action, source_file)
                elif "group" in yaml_obj:
                    groups = yaml_obj["groups"]
                    for row in reader:
                        if row["group"].strip() in groups:
                            for action in actions:
                                if "to_self" in action:
                                    script = script + self.parse_action(action, source_file, row)
                                else:
                                    script = script + self.parse_action(action, source_file)
                elif "type" in yaml_obj:
                    types = yaml_obj["types"]
                    for row in reader:
                        if row["types"].strip() in types:
                            for action in actions:
                                if "to_self" in action:
                                    script = script + self.parse_action(action, source_file, row)
                                else:
                                    script = script + self.parse_action(action, source_file)
                else:
                    for action in actions:
                        script = script + parse_action(action, source_file)
            script = script[0:-1] # Truncate off the last comma
            script = "\n      \"uuid\": " + name + "\n    }\n  ]\n}"
            # script = json.dumps(json.loads(script), indent="  ", sort_keys=False))
            seq_id = http.get_id_back(json.load(script), name)
        else:
            # If this sequence only send the actions of some other sequence
            # but with different types and groups
            send_this = yaml_obj
            for file_name in self.source_files:
                file = yaml.load(open(file_name))
                if n in file:
                    send_this["actions"] = file[n]["actions"]
            seq_id, n = self.make_sequence(send_this, source_file)
            data["children"].append(n)
        data["id"] = seq_id
        stor.add_data(data)
        return (seq_id, name)

    def make_regimen(self, yaml_obj, source_file, name = None):
        """regimen : A yaml object that includes this:
             schedule: [{group: [optional], type: [optional], days: [], times: [], actions: <<list of actions or name of sequence>>}
             OR
             schedule: [{group: [optional], type: [optional], every: 4, unit: "minutes/hours/days/weeks/months/years", actions: <<list of actions or name of sequence>>}
           returns : The ID of the sequence sent, returned from FarmBot

           This function turns a list of actions into a YAML sequence with a
           program-set name, then turns it into a CeleryScript command, sends
           it off and gets the ID back, and writes the YAML sequence object
           with its name and ID to internal storage."""
        if type(name) is not None:
            changed, id = self.check_change(yaml_obj, name)
            if not changed:
                return (id, name)

        script = "{"
        script = script + "\n  \"color\": " + self.default_value(regimen, "color") + ","
        name = ""
        auto = 1 # not-zero is true
        if "name" in yaml_obj:
            name = yaml_obj["name"]
            auto = 0 # zero is false
        else:
            name = stor.unique_name()
        script = script + "\n  \"name\": " + name + ","
        data = {"name" : name, "auto": auto, "kind" : "regimen", "hash":hash(json.dumps(yaml_obj)), "children":[]}

        list_of_sequences = [] # [(seq_id : , time_offsets : [])]

        schedule = yaml_obj["schedule"]

        for sequence in schedule:
            send_this = {"actions" : sequence["actions"]}
            # Make sure the sequence object for the regimen has the right
            # groups and types in it.
            if "groups" in schedule:
                send_this["groups"] = sequence["groups"]
            if "types" in schedule:
                send_this["types"] = sequence["types"]
            if "groups" in sequence:
                send_this["groups"] = sequence["groups"]
            if "types" in sequence:
                send_this["types"] = sequence["types"]
            if type(sequence["actions"]) is not str:
                send_this["actions"] = sequence["actions"]
            else:
                for file_name in self.source_files:
                    file = yaml.load(open(file_name))
                    if n in file:
                        send_this["actions"] = file[n]["actions"]
                        send_this["name"] = n
            id, n = self.make_sequence(send_this, source_file)
            data["children"].append(n)
            list_of_sequences.append({"id":sequence_id,"time_offsets": self.calc_time_offsets(sequence)})
            # Format all the sequences and their times for the regimen
            script = script + "\n  \"regimen_items\": [ "
            for sequence in list_of_sequences:
                time_offsets = self.calc_time_offsets(schedule["days"], schedule["times"])
                for offset in time_offsets:
                    script = script + "\n    {"
                    script = script + "\n      \"time_offset\": " + time + ","
                    script = script + "\n      \"sequence_id\": " + sequence[0]
                    script = script + "\n    },"
            script = script[0:-1] # Truncate off the last comma
            script = script + "\n  ], \n  \"uuid\": "+name+"\n}"
            reg_id = http.get_id_back(json.load(script), name)
            data["id"] = reg_id
            stor.add_data(data)
            return (reg_id, name)

    def make_farm_event(self, yaml_obj, source_file, name):
        """yaml_obj : An YAML object we already know is an event.
           returns : The ID of the event sent, returned from FarmBot

           This function turns a list of actions into a YAML event with a
           program-set name, then turns it into a CeleryScript command, sends
           it off and gets the ID back, and writes the YAML sequence object
           with its name and ID to internal storage."""

        if type(name) is not None:
            changed, id = self.check_change(yaml_obj, name)
            if not changed:
                return (id, name)

            data = {"name" : name, "auto": 0, "kind" : "farm_event", "hash":hash(json.dumps(yaml_obj)), "children":[]}
            script  = script + "\n  \"start_time\" : \"" + self.format_time(yaml_obj["start_time"]) + "\","
            if "repeat_event" in yaml_obj:
           # The following is a field in Farm Events:
           # repeat_event: {every: default 1, unit = "minutes/hours/days/weeks/months/years", until: ???}
                script = script + "\n  \"end_time\" : \"" + self.format_time(yaml_obj["repeat_event"]["until"]) + "\","
                script = script + "\n  \"repeat\" : " + self.default_value(yaml_obj["repeat_event"], "every") + "\","
                script = script + "\n  \"time_unit\" : \"" + yaml_obj["repeat_event"]["unit"] + "\","
            else:
               script = script + "\n  \"time_unit\" : " + "\"never\","
               script = script + "\n  \"repeat\" : " + "\"1\","
            id = -1
            n = ""
            if "schedule" in yaml_obj:
                id, n = self.make_regimen({"schedule" : yaml_obj["schedule"]}, source_file)
                script = script + "\n  \"executable_type\" : " + "\"regimen\","
            elif "actions" in yaml_obj:
                if type(yaml_obj["actions"]) is not str:
                    id, n = self.make_sequence({"actions" : yaml_obj["actions"]}, source_file)
                    script = script + "\n  \"executable_type\" : " + "\"sequence\","
                else:
                    id, type, n = self.obj_from_name(yaml_obj["actions"])
                    script = script + "\n  \"executable_type\" : " + "\"" + type + "\","
            script = script + "\n  \"executable_id\" : " + str(id) +  "\n  \"uuid\": "+name+"\n}"
            data["children"].append(n)
            event_id = http.get_id_back(json.load(script),name)
            data["id"] = event_id
            # When converting an int to a bool, the boolean value is True for all integers except 0.
            # auto = false
            stor.add_data(data)
            return
