"""This class handles translating YAML into CeleryScript for both
   Sequences and Regimens."""

import yaml
import csv

import json
import http_requests as http
import datetime
import handle_internal_storage as stor


device_id = api_token_gen.token_data['token']['unencoded']['bot']
mqtt_host = api_token_gen.token_data['token']['unencoded']['mqtt']
token = api_token_gen.token_data['token']['encoded']

class ActionHandler():
    PATH = ".internal_storage/farmbot_commands.txt"
    def __init__(self, yaml_file_names, default_settings=None, csv_file_name=None):
        """yaml_file_names  : YAML files
           default_settings : a single file containing
           csv_file_names   : a list of CSV files holding map coordinates"""
        self.source_files = {} # {file : {pin_alias : PIN}}
        self.seq_store = {} # {sequence name : internal YAML object}
        self.reg_store = {} # {regimen name : internal YAML object}
        self.evt_store = {} # {executable_id : internal YAML object}
        self.map = csv_file_name
        self.names = 0  # to assign unique names, will need to be replaced later
                        # when we start storing internal data
        self.pins = {}
        self.settings = (1, 50, 0, 0, 0, 0) #scale, speed, z, x_offset, y_offset, z_offset
        self.get_defaults(yaml_file_names, default_settings)
        self.load_actions()

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
        for f in yaml_file_names:
            file = yaml.load(open(f, 'r'))
            self.source_files[f] = {}
            for key in file:
                if type(file[key]) is str: # aka it is a setting for a PIN
                    self.source_files[f][key] = file[key]
                if type(file[key]) is list: # aka it refers to other files
    def obj_from_name(self, name):
        """name : the name of a YAML object
           returns : the ID of the sent object, and its type

           This function figues out if a name refers to a regimen or a sequence,
           calls the right function, and give returns the ID."""
        for file_name in self.source_files:
            file = yaml.load(open(file_name))
            if name in file:
                if "schedule" in file[name]:
                    id, name = make_regimen(file[name], name)
                    return (id, "regimen", name)
                elif "actions" in file[name]:
                    if file[name["actions"]] is not str:
                        id, name = make_sequence(file[name], name)
                        return (id, "sequence", name)
                    else:
                        return obj_from_name(file[name["actions"]])
                else:
                    print("Invalid format for object",name)

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
                    self.make_farm_event(file[name], name):
                elif "schedule" in yaml_obj:
                    self.make_regimen(file[name], name)
                elif "actions" in yaml_obj:
                    self.make_sequence(file[name], name)
                else:
                    print("Invalid format for object:", name)


    def calc_time_offsets(self, schedule): #test version, 30 days per month, millisecond as unit
    """regimen : A yaml object that includes this:
         schedule: [{group: [optional], type: [optional], days: [], times: [], actions: <<list of actions or name of sequence>>}
         OR
         schedule: [{group: [optional], type: [optional], every: 4, unit: "minutes/hours/days/weeks/months/years", actions: <<list of actions or name of sequence>>}
       returns : a list of integers that are time_offset(s) for CeleryScript"""
        if "days" in schedule:
            days = schedule["days"]
            times = schedule["times"]
            for x in days:
               if x == datetime.datetime.now().day:
                   if cal_min(times) > 0:
                      return cal_min(times)
                   elif x == days[-1]:
                       idays = (30 - datetime.datetime.now().day + x) * 24 * 60 * 60 * 1000
                       itimes = cal_min(times)
                       return itimes + idays
             elif x > datetime.datetime.now().day:
                  idays = (x - datetime.datetime.now().day) * 24 * 60 * 60 * 1000
                  itimes = cal_min(times)
                  return itimes + idays
             elif x == days[-1]:
                  idays = (30 - datetime.datetime.now().day + x) * 24 * 60 * 60 * 1000
                  itimes = cal_min(times)
                  return itimes + idays
        elif "every" in schedule:
            every = schedule["every"]
            unit = schedule["unit"]
            last_modified = schedule["last_modified"]
            if not last_modified:
                next_time = datetime.datetime.now()
                schedule["last_modified"] = datetime.datetime.now()
            else:    
                if datetime.datetime.now() > last_modified:
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
                next_time = unix_time_millis(last_modified) + period
                schedule["last_modified"] = datetime.utcfromtimestamp(next_time)
            return next_time

   def cal_min(self,ttime):
      if int(ttime[0:2]) > datetime.datetime.now().hour:
         itime = ((int(ttime[0:2]) - datetime.datetime.now().hour) * 60 *60 + (int(ttime[3:5]) - datetime.datetime.now().minute) * 60 - datetime.datetime.now().second) * 1000 - datetime.datetime.now().microsecond * 0.001
         return int(itime)
      elif int(ttime[0:2]) == datetime.datetime.now().hour and int(ttime[3:5]) > datetime.datetime.now().minute:
         itime = ((int(ttime[0:2]) - datetime.datetime.now().hour) * 60 *60 + (int(ttime[3:5]) - datetime.datetime.now().minute) * 60 - datetime.datetime.now().second) * 1000 - datetime.datetime.now().microsecond * 0.001
         return int(itime)
      else:
         itime = (((int(ttime[0:2]) - datetime.datetime.now().hour) * 60 *60 + (int(ttime[3:5]) - datetime.datetime.now().minute) * 60 - datetime.datetime.now().second) * 1000 - datetime.datetime.now().microsecond * 0.001)
         return int(itime)

    epoch = datetime.datetime.utcfromtimestamp(0)
    def unix_time_millis(dt):
        """convert datetime to miliseconds"""
        return (dt - epoch).total_seconds() * 1000.0
      
    def default(self,yaml_obj, field):
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

    def translate(self,yaml_obj, field):
        if field == "time_unit":
            if yaml_obj["unit"] = "days":
                return "daily"
            else:
                return yaml_obj["unit"][0:-1] + "ly"

    def pin_name(self, pin):
        if pin in self.pins:
            return self.pins[pin]
        else:
            return pin

    def parse_coord(x=0,y=0,z=0,row=None):
        if row == None:
            return "{\"kind\": \"coordinate\",\"args\": {\"x\": "+ x + "\"y\": " + y + "\"z\": " + z + "} },"
        else:
            script = "{\"kind\": \"coordinate\",\"args\": {\"x\": "+ row["x"] + "\"y\": " + row["y"] + "\"z\": "
            if row["z"].strip()!="":
                script = script + row["z"] + "} },"
            else:
                script = script + default({},"z") + "} },"
            return script

    def parse_action(self,action,row=None):
        script = ""
        if "move_abs" in action:
            script = script + "{\"kind\":\"move_absolute\","
            script = script + "\"args\": {\"location\": " + parse_coord(self.default(action,"x"), self.default(action,"y"), self.default(action,"z"))
            script = script + "\"args\": {\"offset\": " + parse_coord(self.default(action,"x_off"), self.default(action,"y_off"), self.default(action,"z_off"))
            script = script + "\"speed\": " + self.default(action, "speed") + "},},"
        elif "move_rel" in action:
            script = script + "{\"kind\":\"move_relative\","
            script = script + "\"args\": {\"location\": " + parse_coord(self.default(action,"x"), self.default(action,"y"), self.default(action,"z"))
            script = script + "\"speed\": " + self.default(action, "speed") + "},},"
        elif "find_home" in action:
            script = script + "{\"kind\":\"find_home\",{\"args\": { \"axis\": "
            allowed_axis = action["find_home"]
            if "x" in allowed_axis:
                script = script + "\"x\","
            if "y" in allowed_axis:
                script = script + "\"y\","
            if "z" in allowed_axis:
                script = script + "\"z\","
            else:
                script = script + "\"all\","
            script = script + "\"speed\": " + self.default(action, "speed") + "},},"
        elif "message"in action:
            # code here
        elif "wait" in action:
            return "{\"kind\": \"wait\", \"args\": { \"milliseconds\": \""+ action["wait"] +"\" } },"
        elif "read_pin" in action:
            args = action["read_pin"]
            script = script + "{\"kind\": \"read_pin\", \"args\": { "
            if "label" in action["read_pin"]:
                script = script + "\"label\": \""+ args["label"] +"\","
            script = script + "\"pin_number\": \""+ self.pin_name(args["pin"]) +"\"," "\"pin_mode\": \""+ args["mode"] +"\","" + " } },"
        elif "write_pin" in action:
            script = script + "{\"kind\": \"write_pin\", \"args\": { "
            script = script + "\"pin_mode\": \""+ args["mode"] +"\","
            script = script + "\"pin_number\": \""+ self.pin_name(args["pin"]) +"\"," "\"pin_value\": \""+ action["value"] +"\","" + " } },"
            # Note, I'm not sure if the pin_value for Digital mode can be a string or if it must be an integer
        elif "to_self" in action:
            script = script + "{\"kind\":\"move_absolute\","
            script = script + "\"args\": {\"location\": " + parse_coord(row=row)
            script = script + "\"args\": {\"offset\": " + parse_coord(self.default(action,"x_off"), self.default(action,"y_off"), self.default(action,"z_off"))
            script = script + "\"speed\": " + self.default(action, "speed") + "},},"
        elif "to_plant" in action:
            # code here
        elif "if" in action:
            # difficult code here
        else:
            raise Error("The action " + action.keys()[0] + " is undefined.")
        return script

    def check_change(yaml_obj, name):
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
                                if check_change(file[name], child):
                                    stor.delete_object(name)
                                    return (True, id)
                return (False, id)
            else: # Already exists in storage and has changed
                stor.delete_object(name)
                return (True, id)
        else:
            return (False, id)

    def make_sequence(self, yaml_obj, name = None):
        """sequence : Includes or is a list of actions.
           returns : The ID of the sequence sent, returned from FarmBot

           This function turns a list of actions into a YAML sequence with a
           program-set name, then turns it into a CeleryScript command, sends
           it off and gets the ID back, and writes the YAML sequence object
           with its name and ID to internal storage."""
        if type(name) is not None:
            changed, id = check_change(yaml_obj, name)
            if not changed:
                return (id, name)

        script = "{"
        name = ""
        auto = 1 # not-zero is true
        seq_id = -1
        if "name" in yaml_obj":
            name = yaml_obj["name"]
            auto = 0 # zero is false
        else:
            name = unique_name()
        script = script + "\n  \"name\": " + name + ","
        data = {"name" : name, "auto": auto, "kind" : "regimen", "hash":hash(json.dumps(yaml_obj)), "children":[]}

        script =  = script + "\n  \"body\": [ \n    {"
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
                                    script = script + parse_action(action, row)
                                else:
                                    script = script + parse_action(action)
                elif "group" in yaml_obj:
                    groups = yaml_obj["groups"]
                    for row in reader:
                        if row["group"].strip() in groups:
                            for action in actions:
                                if "to_self" in action:
                                    script = script + parse_action(action, row)
                                else:
                                    script = script + parse_action(action)
                elif "type" in yaml_obj:
                    types = yaml_obj["types"]
                    for row in reader:
                        if row["types"].strip() in types:
                            for action in actions:
                                if "to_self" in action:
                                    script = script + parse_action(action, row)
                                else:
                                    script = script + parse_action(action)
                else:
                    for action in actions:
                        script = script + parse_action(action)
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
            seq_id, n = make_sequence(send_this)
            data["children"].append(n)
        data["id"] = seq_id
        stor.add_data(data)
        return (seq_id, name)

    def make_regimen(self, yaml_obj, name = None):
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
            changed, id = check_change(yaml_obj, name)
            if not changed:
                return (id, name)

        script = "{"
        script = script + "\n  \"color\": " + default_value(regimen, "color") + ","
        name = ""
        auto = 1 # not-zero is true
        if "name" in yaml_obj":
            name = yaml_obj["name"]
            auto = 0 # zero is false
        else:
            name = unique_name()
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
            id, n = make_sequence(send_this)
            data["children"].append(n)
            list_of_sequences.append({"id":sequence_id,"time_offsets": calc_time_offsets(sequence)})
            # Format all the sequences and their times for the regimen
            script = script + "\n  \"regimen_items\": [ "
            for sequence in list_of_sequences:
                time_offsets = calc_time_offsets(schedule["days"], schedule["times"])
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


    def make_farm_event(self, yaml_obj, name):
        """yaml_obj : An YAML object we already know is an event.
           returns : The ID of the event sent, returned from FarmBot

           This function turns a list of actions into a YAML event with a
           program-set name, then turns it into a CeleryScript command, sends
           it off and gets the ID back, and writes the YAML sequence object
           with its name and ID to internal storage."""

        if type(name) is not None:
            changed, id = check_change(yaml_obj, name)
            if not changed:
                return (id, name)

           data = {"name" : name, "auto": 0, "kind" : "farm_event", "hash":hash(json.dumps(yaml_obj)), "children":[]}
           script  = script + "\n  \"start_time\" : \"" + yaml_obj["start_time"] + "\","
           if "repeat_event" in yaml_obj:
           # The following is a field in Farm Events:
           # repeat_event: {every: default 1, unit = "minutes/hours/days/weeks/months/years", until: ???}
               script = script + "\n  \"end_time\" : \"" + cal_min(yaml_obj["repeat_event"]["until"]) + "\","
               script = script + "\n  \"repeat\" : " + default_value(yaml_obj["repeat_event"], "every") + "\","
               script = script + "\n  \"time_unit\" : \"" + yaml_obj["repeat_event"]["unit"] + "\","
           else:
               script = script + "\n  \"time_unit\" : " + "\"never\","
               script = script + "\n  \"repeat\" : " + "\"1\","
           id = -1
           n = ""
           if "schedule" in yaml_obj:
               id, n = self.make_regimen({"schedule" : yaml_obj["schedule"]})
               script = script + "\n  \"executable_type\" : " + "\"regimen\","
           elif "actions" in yaml_obj:
               if type(yaml_obj["actions"]) is not str:
                   id, n = self.make_sequence({"actions" : yaml_obj["actions"]})
                   script = script + "\n  \"executable_type\" : " + "\"sequence\","
               else:
                   id, type, n = obj_from_name(yaml_obj["actions"])
                   script = script + "\n  \"executable_type\" : " + "\"" + type + "\","
           script = script + "\n  \"executable_id\" : " + str(id) +  "\n  \"uuid\": "+name+"\n}"
           data["children"].append(n)
           event_id = http.get_id_back(json.load(script),name)
           data["id"] = event_id
           # When converting an int to a bool, the boolean value is True for all integers except 0.
           # auto = false

           stor.add_data(data)
           return
