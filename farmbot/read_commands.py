"""This class handles translating YAML into CeleryScript for both
   Sequences and Regimens."""

import yaml
import csv

import json
import http_requests as http
import datetime
from time import timezone
import handle_internal_storage as stor
from hashlib import sha224
import pytz
# device_id = api_token_gen.token_data['token']['unencoded']['bot']
# mqtt_host = api_token_gen.token_data['token']['unencoded']['mqtt']
# token = api_token_gen.token_data['token']['encoded']

class ActionHandler():
    PATH = "../.internal_data/farmbot_commands.yaml"
    def __init__(self, yaml_file_names, csv_file_name=None):
        """yaml_file_names  : a list of YAML files
           csv_file_names   : a list of CSV files holding map coordinates"""
        self.source_files = {} # {file : {pin_aliases : {alias : PIN}}}
        self.map = csv_file_name
        self.settings = (1, 50, 0, 0, 0, 0) #scale, speed, z, x_offset, y_offset, z_offset
        self.get_defaults(yaml_file_names)
        # self.load_actions()

    def get_defaults(self, yaml_file_names):
        sources = set(yaml_file_names)
        for file_name in sources:
            file = yaml.load(open(file_name, 'r'))
            self.source_files[file_name] = {}
            self.source_files[file_name]["pin_aliases"] = {}
            if file["options"] is not None and "options" in file:
                if "pin_aliases" in file["options"]:
                    for alias, pin in file["options"]["pin_aliases"].items():
                        self.source_files[file_name]["pin_aliases"][alias] = pin
                if "scale" in file["options"]:
                    strings = file["options"]["scale"].split()
                    self.source_files[file_name]["scale"] = 1
                    if strings[1] == "cm":
                        self.source_files[file_name]["scale"] = int(strings[0])*10
                    if strings[1] == "mm":
                        self.source_files[file_name]["scale"] = int(strings[0])
                    if strings[1] == "m":
                        self.source_files[file_name]["scale"] = int(strings[0])*1000
                else:
                    self.source_files[file_name]["scale"] = 1
                if "default_speed" in file["options"]:
                    self.source_files[file_name]["speed"] = file["options"]["default_speed"]
                else:
                    self.source_files[file_name]["speed"] = 50
                if "default_z" in file["options"]:
                    self.source_files[file_name]["z"] = file["options"]["default_z"]
                else:
                    self.source_files[file_name]["speed"] = 0
                if "default_x_offset" in file["options"]:
                    self.source_files[file_name]["x_off"] = file["options"]["default_x_offset"]
                else:
                    self.source_files[file_name]["x_off"] = 0
                if "default_y_offset" in file["options"]:
                    self.source_files[file_name]["y_off"] = file["options"]["default_y_offset"]
                else:
                    self.source_files[file_name]["y_off"] = 0
                if "default_z_offset" in file["options"]:
                    self.source_files[file_name]["z_off"] = file["options"]["default_z_offset"]
                else:
                    self.source_files[file_name]["z_off"] = 0
            if file["options"] is not None and "other_files" in file["options"]: # aka it refers to other files
                    sources.union(set(file["options"]["other_files"]))

    def obj_from_name(self, name):
        """name : the name of a YAML object
           returns : the ID of the sent object, and its type

           This function figues out if a name refers to a regimen or a sequence,
           calls the right function, and give returns the ID."""
        for file_name in self.source_files:
            file = yaml.load(open(file_name))
            if name in file:
                if "schedule" in file[name]:
                    id, name, this_needs_csv = self.make_regimen(file[name], file_name, name)
                    return (id, "Regimen", name, this_needs_csv)
                elif "actions" in file[name]:
                    if file[name]["actions"] is not str:
                        id, name, this_needs_csv = self.make_sequence(file[name], file_name, name)
                        return (id, "Sequence", name, this_needs_csv)
                    else:
                        return self.obj_from_name(file[name]["actions"])
                else:
                    print("Invalid format for object", name)

    def load_commands(self):
        """Modifies self.source_files, self.seq_script, and self.reg_script
           corrosponds to 'process_a_file' in the pseudocode"""
        for source in self.source_files:
            f = open(source, "r")
            file = yaml.load(f)
            for name in file:
                if "start_time" in file[name]:
                    self.make_farm_event(file[name], source, name)
                elif "schedule" in file[name]:
                    print(self.make_regimen(file[name], source, obj_name=name))
                elif "actions" in file[name]:
                    print(self.make_sequence(file[name], source, obj_name=name))
                else:
                    pass
            f.close()

    def calc_time_offsets(self, schedule):
        """regimen : A yaml object that includes this:
           schedule: {group: [optional], type: [optional], days: [], times: [], actions: <<list of actions or name of sequence>>}
           OR
           schedule: {group: [optional], type: [optional], every: 4, unit: "minutes/hours/days/weeks/months/years", max: 10, actions: <<list of actions or name of sequence>>}
           returns : a list of integers that are time_offset(s) for CeleryScript"""
        time_offsets = []
        if "days" in schedule:
            days = schedule["days"]
            times = []
            for time in schedule["times"]:
                times.append(int(time[0:2])*60*60*1000 + int(time[3:])*60*1000)
            now = datetime.datetime.now()
            for day in days:
                begin = (day - 1) * 24*60*60*1000
                for time in times:
                    time_offsets.append(begin+time)
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
            for i in range(0,schedule["max"]):
                time_offsets.append(i*period)
        return time_offsets

    def format_time(self, time):
        """time: DD/MM/YYYY 23:00
           returns: ISO 8601 date representation, from local time on the user's desktop."""
        # Attributes: year, month, day, hour, minute, second, microsecond, and tzinfo.
        tz = datetime.datetime.now().astimezone().tzinfo
        tzaware_dt = datetime.datetime(int(time[6:10]), int(time[3:5]), int(time[0:2]),
         int(time[11:13]), int(time[14:]), tzinfo=tz)
        string = tzaware_dt.isoformat()
        string = string[:19]+".000"+string[19:]
        # string = time[6:10]+"-"+time[3:5]+"-"+time[0:2]+"T"+time[11:]+":00"
        # tz = datetime.datetime.utcnow().isoformat()
        # print("\n tz type", type(tz))
        # print("\n", tz, "\n")
        # print("\n time " + string + tz[19:] + "\n")
        return tzaware_dt.isoformat()


    def default(self, yaml_obj, field, source_file):
        if field == "color":
            if "color" in yaml_obj:
                return yaml_obj["color"]
            else:
                return "gray"
        elif field == "every":
            if "every" in yaml_obj:
                return str(yaml_obj["every"])
            else:
                return str(1)
        elif field == "speed":
            if "speed" in yaml_obj:
                return str(yaml_obj["speed"])
            else:
                return str(self.source_files[source_file]["speed"])
        # Note: The default coordinates are unscaled.
        elif field == "z":
            if "z" in yaml_obj:
                return int(yaml_obj["z"])
            else:
                return int(self.source_files[source_file]["z"])
        elif field == "x_off":
            if "x_off" in yaml_obj:
                return int(yaml_obj["x_off"])
            else:
                return int(self.source_files[source_file]["x_off"])
        elif field == "y_off":
            if "y_off" in yaml_obj:
                return int(yaml_obj["y_off"])
            else:
                return int(self.source_files[source_file]["y_off"])
        elif field == "z_off":
            if "z_off" in yaml_obj:
                return int(yaml_obj["z_off"])
            else:
                return int(self.source_files[source_file]["z_off"])

    def translate(self, yaml_obj, field):
        if field == "every":
            if yaml_obj["unit"] == "days":
                return "daily"
            else:
                return yaml_obj["unit"][0:-1] + "ly"
        elif field == "digi_ana":
            if yaml_obj["mode"] == "D":
                return "0"
            else:
                return "1"
        elif field == "pin_value":
            if yaml_obj["value"] == "OFF":
                return "0"
            elif yaml_obj["value"] == "ON":
                return "1"
            else:
                return yaml_obj["value"]
        elif field == "peri_sens":
            if yaml_obj == "p":
                return "\"Peripheral\""
            elif yaml_obj == "s":
                return "\"Sensor\""
            else:
                print("error 924")
        elif field == "condition":
            if yaml_obj == "=":
                return "\"is\""
            elif yaml_obj == "<":
                return "\"<\""
            elif yaml_obj == ">":
                return "\">\""
            elif yaml_obj == "!=":
                return "\"not\""
            else:
                print("error 324")

    def pin_name(self, pin, source_file):
        if pin in self.source_files[source_file]["pin_aliases"]:
            args = self.source_files[source_file]["pin_aliases"][pin]
            script = "{kind: \"named_pin\", args: { pin_id:" + str(args[0], "peri_sens")
            script = script + ", pin_type: \"" + self.translate(args[1], "peri_sens") + "\" } },"
            return script
        else:
            return str(pin)

    def parse_coord(self, coords=None,row=None, source_file=None):
        """coords = {x:0, y:0, z:0} or {x_off:0, y_off:0, z_off:0}
           row = A CSV for of a plant
           """
        if row is not None:
            # If we are supposed to move to the location of a plant, defined by a CSV row which may have no "z" provided.
            scale = self.source_files[source_file]["scale"]
            script = "{\"kind\": \"coordinate\",\"args\": {\"x\": "+ str(int(row["x"])*scale) + ",\"y\": " + str(int(row["y"])*scale) + ",\"z\": "
            if row["z"].strip()!="":
                script = script + str(int(row["z"])*scale) + "} },"
            else:
                script = script + str(self.default({},"z", source_file)*scale) + "} },"
            return script
        elif coords is not None:
            # If we are provided coords
            scale = self.source_files[source_file]["scale"]
            if "x" in coords:
                return "{\"kind\": \"coordinate\",\"args\": {\"x\": "+ str(coords["x"]*scale) + ",\"y\": " + str(coords["y"]*scale) + ",\"z\": " + str(self.default(coords,"z",source_file)*scale) + "} },"
            else:
                return "{\"kind\": \"coordinate\",\"args\": {\"x\": "+ str(self.default(coords,"x_off",source_file)*scale) + ",\"y\": " + str(self.default(coords,"y_off",source_file)*scale) + ",\"z\": " + str(self.default(coords,"z_off",source_file)*scale) + "} },"


    def parse_action(self,action, source_file, row=None):
        # The row is only needed for the action to_self
        script = ""
        if type(action) is str:
            # This means the action is actually another sequence
            for source in self.source_files:
                f = open(source, 'r')
                file = yaml.load(f)
                f.close()
                if action in file:
                    id, n, child_needs_csv = self.make_sequence(file[action], source, obj_name=action)
                    script = script + "{ \"kind\": \"execute\", \"args\": { \"sequence_id\": " + str(id) + "} },"
                return (script, n, child_needs_csv)
        elif "move_abs" in action:
            args = action["move_abs"]
            script = script + "{\"kind\":\"move_absolute\","
            script = script + "\"args\": {\"location\": " + self.parse_coord(coords=args,source_file=source_file)
            script = script + "\"offset\": " + self.parse_coord(coords=args,source_file=source_file)
            script = script + "\"speed\": " + self.default(args, "speed",source_file) + "} },"
        elif "move_rel" in action:
            args = action["move_rel"]
            script = script + "{\"kind\":\"move_relative\","
            script = script + "\"args\": {\"x\" :" + str(args["x"]) + ",\"y\":" + str(args["y"]) + ",\"z\":" + str(self.default(args,"z",source_file))
            script = script + ",\"speed\": " + self.default(args, "speed",source_file) + "} },"
        elif "find_home" in action:
            args = action["find_home"]
            if "all" in args or len(args)==0:
                script = script + "{\"kind\":\"find_home\",\"args\": { \"axis\": "
                script = script + "\"all\","
                script = script + "\"speed\": " + self.default(args, "speed",source_file) + "} },"
            else:
                for coord in args:
                    script = script + "{\"kind\":\"find_home\",\"args\": { \"axis\": "
                    script = script + "\""+coord+"\","
                    script = script + "\"speed\": " + self.default(args, "speed",source_file) + "} },"
        elif "wait" in action:
            return "{\"kind\": \"wait\", \"args\": { \"milliseconds\": "+ str(action["wait"]) + " } },"
        elif "read_pin" in action:
            args = action["read_pin"]
            script = script + "{\"kind\": \"read_pin\", \"args\": { "
            if "label" in args:
                script = script + "\"label\": \""+ args["label"] +"\","
            script = script + "\"pin_number\": "+ self.pin_name(args["pin"], source_file) +", \"pin_mode\": "+ self.translate(args, "digi_ana") + " } },"
        elif "write_pin" in action:
            args = action["write_pin"]
            script = script + "{\"kind\": \"write_pin\", \"args\": { "
            script = script + "\"pin_mode\": "+ self.translate(args, "digi_ana") +","
            script = script + "\"pin_number\": "+ self.pin_name(args["pin"], source_file) +", \"pin_value\": "+ str(self.translate(args, "pin_value")) + " } },"
            # Note, I'm not sure if the pin_value for Digital mode can be a string or if it must be an integer
        elif "to_self" in action:
            args = action["to_self"]
            script = script + "{\"kind\":\"move_absolute\","
            script = script + "\"args\": {\"location\": " + self.parse_coord(row=row,source_file=source_file)
            script = script + "\"offset\": " + self.parse_coord(coords=args,source_file=source_file)
            script = script + "\"speed\": " + self.default(action, "speed",source_file) + "} },"
        elif "to_plant" in action:
            try:
                with open(self.map, "r") as csv_file:
                    reader = csv.DictReader(csv_file)
                    args = action["to_plant"]
                    for row in reader:
                        if row["name"].strip() == action["to_plant"]["name"]:
                            script = script + "{\"kind\":\"move_absolute\","
                            script = script + "\"args\": {\"location\": " + self.parse_coord(row=row,source_file=source_file)
                            script = script + "\"offset\": " + self.parse_coord(coords=args,source_file=source_file)
                            script = script + "\"speed\": " + self.default(args, "speed",source_file) + "} },"
            except:
                raise Exception("A \"to_plant\" command requires a CSV file.")
        elif "if" in action:
            # args : {"cond" :  , "then" :  , "else" :  }
            args = action["if"]
            condition = args["cond"].split()
            child_needs_csv = False
            children = []

            script = script + "{\"kind\": \"_if\", \"args\": { \"lhs\":"
            if condition[0] in ["x","y","z"]:
                script = script + "\"" + condition[0] + "\""
            else:
                script = script + self.pin_name(condition[0],source_file)
            script = script +"," "\"op\": "+ self.translate(condition[1],"condition") +", "
            script = script + "\"rhs\": "+ condition[2] +","

            script = script + "\"_then\": { "
            if type(args["then"]) is str:
                seq_needed = args["then"]
                seq_id = -1
                for source in self.source_files:
                    f = open(source, 'r')
                    file = yaml.load(f)
                    f.close()
                    if seq_needed in file:
                        seq_id, n, needs_csv = self.make_sequence(file[seq_needed], source, obj_name=seq_needed)
                        children.append(n)
                        child_needs_csv = (child_needs_csv or needs_csv)
                        break
                script = script + "\"kind\":\"execute\","
                script = script + "\"args\": {\"sequence_id\": " + str(seq_id) +" } },"
            else:
                script = script + "\"kind\":\"nothing\", \"args\": { } } } "
            # script = script + "\"args\": { " + "\"," + " } } } }"
            script = script + "\"_else\": { "
            if "else" in args:
                seq_needed = args["else"]
                seq_id = -1
                for source in self.source_files:
                    f = open(source, 'r')
                    file = yaml.load(f)
                    f.close()
                    if seq_needed in file:
                        seq_id, n, needs_csv = self.make_sequence(file[seq_needed], source, obj_name=seq_needed)
                        children.append(n)
                        child_needs_csv = (child_needs_csv or needs_csv)
                        break
                script = script + "\"kind\":\"execute\","
                script = script + "\"args\": {\"sequence_id\": " + str(seq_id) +" } } }"
            else:
                script = script + "\"kind\":\"nothing\", \"args\": { } } } } "
            # script = script + "\"args\": { " + "\"," + " } } } }"
            return (script, children, child_needs_csv)
        else:
            raise Exception("The action " + action.keys()[0] + " is undefined.")
        return script


    def check_change(self, yaml_obj, name):
        """Checks if an object or any object it depends on has changed.
           IF an object has been changed, it automatically deletes that object from storage.
           yaml_obj: the new object definition
           name: the name of the object
           hash: the new hash of the object"""
        existance, id, stored_hash, children = stor.check_exist(name)
        f = open(self.map, 'r')
        print("looking if exists: ",name)
        if existance:
            # needs_a_csv, csv_hash = stor.check_need_csv(name)
            # if needs_a_csv:
                # new_csv_hash = sha224((f.read()).encode()).hexdigest()
            new_hash = sha224(json.dumps(yaml_obj).encode()).hexdigest()
            str_obj = json.dumps(yaml_obj)
            # If the hash of the object has not changed and its CSV, if it relies on one, has not changed.
            if (str(stored_hash) == new_hash):
            # if (str(stored_hash) == new_hash) and not (needs_a_csv and csv_hash != new_csv_hash):
                # If the object has user-defined children, check if its children changed.
                for old_child in children:
                    if old_child[:5] != "auto_":
                        for source in self.source_files:
                            f = open(source, mode='r+')
                            file = yaml.load(f)
                            f.close()
                            if old_child in file:
                                if self.check_change(file[old_child], old_child)[0]:
                                    # If the child has changed, we only need to delete the parent.
                                    # The child will be deleted by its own call to check_change
                                    # when we re-send the parent.
                                    stor.delete_object(name)
                                    # If one of its children have changed
                                    print("result 1",name)
                                    return (True, id)
                # If neither it nor its children have changed
                print("result 2",name)
                return (False, id)
            else:
                # If the raw command's hash has changed or the hash of the CSV it needs has changed.
                stor.delete_object(name)
                print("result 3",name)
                return (True, id)
        else:
            # Does not exist and needs to be made.
            print("result 4",name)
            return (True, id)

    def make_sequence(self, yaml_obj, source_file, obj_name = None):
        """sequence : Includes or is a list of actions.
           returns : The ID of the sequence sent, returned from FarmBot

           This function turns a list of actions into a YAML sequence with a
           program-set name, then turns it into a CeleryScript command, sends
           it off and gets the ID back, and writes the YAML sequence object
           with its name and ID to internal storage."""

        str_obj = json.dumps(yaml_obj)
        needs_a_csv = ("group" in yaml_obj or "type" in yaml_obj or "to_plant" in str_obj or "to_self" in str_obj)
        child_needs_csv = False

        name = ""
        auto = 1 # not-zero is true
        id = -1
        hash = sha224(str_obj.encode()).hexdigest()

        if obj_name is not None:
            if needs_a_csv:
                name = obj_name + "_" + self.map
            else:
                name = obj_name
            changed, id = self.check_change(yaml_obj, name)
            if not changed:
                return (id, obj_name, False)
        else:
            name = stor.unique_name(hash)
            # data = {name : {"auto": auto, "kind" : "sequence", "hash":hash, "children":[] }}
            # Auto-genned names need to be stored immediately by unique_name, and adding
            # should replace names
            # If we discover we need a csv later, we must change our name (and can safely do so)
            # if it is not auto-generated


        script = "{"

        script = script + "\n  \"name\": \"" + name + "\","
        data = {name : {"auto": auto, "kind" : "sequence", "hash":hash, "children":[] }}
        # if needs_a_csv:
            # data["CSV"] = self.map
            # data["csv_hash"] = sha224((f.read()).encode()).hexdigest()

        script = script + "\n  \"body\": [ \n    "
        actions = yaml_obj["actions"]
        if self.map is not None:
            with open(self.map, "r") as csv_file:
                reader = csv.DictReader(csv_file)
                if "groups" in yaml_obj and "types" in yaml_obj:
                    groups = yaml_obj["groups"]
                    types = yaml_obj["types"]
                    for row in reader:
                        if row["group"].strip() in groups or row["type"].strip() in types:
                            for action in actions:
                                # We need the "row" arguement just in case the action is "to_self"
                                if type(action) is str:
                                    s, n, this_needs_csv = self.parse_action(action, source_file, row)
                                    child_needs_csv = (child_needs_csv or this_needs_csv)
                                    script = script + s
                                    data[name]["children"].append(n)
                                elif "if" in action:
                                    s, childern, this_needs_csv = self.parse_action(action, source_file, row)
                                    child_needs_csv = (child_needs_csv or this_needs_csv)
                                    script = script + s
                                    data[name]["children"] = data[name]["children"] + childern
                                else:
                                    script = script + self.parse_action(action, source_file, row)
                elif "groups" in yaml_obj:
                    groups = yaml_obj["groups"]
                    for row in reader:
                        if row["group"].strip() in groups:
                            for action in actions:
                                if type(action) is str:
                                    # This means the action is actually a sub-sequence
                                    s, n, this_needs_csv = self.parse_action(action, source_file)
                                    child_needs_csv = (child_needs_csv or this_needs_csv)
                                    script = script + s
                                    data[name]["children"].append(n)
                                elif "if" in action:
                                    s, childern, this_needs_csv = self.parse_action(action, source_file)
                                    child_needs_csv = (child_needs_csv or this_needs_csv)
                                    script = script + s
                                    data[name]["children"] = data[name]["children"] + childern
                                # We need the "row" arguement just in case the action is "to_self"
                                else:
                                    script = script + self.parse_action(action, source_file, row)
                elif "types" in yaml_obj:
                    types = yaml_obj["types"]
                    for row in reader:
                        if row["type"].strip() in types:
                            for action in actions:
                                if type(action) is str:
                                    # This means the action is actually a sub-sequence
                                    s, n, this_needs_csv = self.parse_action(action, source_file)
                                    child_needs_csv = (child_needs_csv or this_needs_csv)
                                    script = script + s
                                    data[name]["children"].append(n)
                                elif "if" in action:
                                    s, childern, this_needs_csv = self.parse_action(action, source_file)
                                    child_needs_csv = (child_needs_csv or this_needs_csv)
                                    script = script + s
                                    data[name]["children"] = data[name]["children"] + childern
                                # We need the "row" arguement just in case the action is "to_self"
                                else:
                                    script = script + self.parse_action(action, source_file, row)
                else:
                    # There is a map provided, but we don't need it.
                    for action in actions:
                        if type(action) is str:
                            s, n, this_needs_csv = self.parse_action(action, source_file)
                            child_needs_csv = (child_needs_csv or this_needs_csv)
                            script = script + s
                            data[name]["children"].append(n)
                        elif "if" in action:
                            s, childern, this_needs_csv = self.parse_action(action, source_file)
                            child_needs_csv = (child_needs_csv or this_needs_csv)
                            script = script + s
                            data[name]["children"] = data[name]["children"] + childern
                        else:
                            script = script + self.parse_action(action, source_file)
        else:
            # There is no map provided, and we assume we don't need one.
            for action in actions:
                if type(action) is str:
                    s, n, this_needs_csv = self.parse_action(action, source_file)
                    child_needs_csv = (child_needs_csv or this_needs_csv)
                    script = script + s
                    data[name]["children"].append(n)
                elif "if" in action:
                    s, childern, this_needs_csv = self.parse_action(action, source_file)
                    child_needs_csv = (child_needs_csv or this_needs_csv)
                    script = script + s
                    data[name]["children"] = data[name]["children"] + childern
                else:
                    script = script + self.parse_action(action, source_file)

        script = script[:-1] # Truncate off the last comma of the last action
        # script = script + "\n      \"uuid\": \"" + name + "\"\n    }\n  ]\n}"
        script = script + "\n  ]\n}"
        # script = json.dumps(json.loads(script), indent="  ", sort_keys=False)

        file = open("celeryscript.txt",'a')
        file.write(script)
        # file.write(json.dumps(json.loads(script), indent="  ", sort_keys=False))
        file.close()
        # print("\n",type(json.loads(script)),"\n")

        # If one of its children needs a CSV file
        # if not needs_a_csv and child_needs_csv:
            # data["CSV"] = self.map
            # data["csv_hash"] = sha224((f.read()).encode()).hexdigest()

        id = http.new_command(json.loads(script), "sequence")
        data[name]["id"] = id
        stor.add_data(data)

        return (id, name, (needs_a_csv or child_needs_csv))

    def make_regimen(self, yaml_obj, source_file, obj_name = None):
        """regimen : A yaml object that includes this:
             schedule: [{group: [optional], type: [optional], days: [], times: [], actions: <<list of actions or name of sequence>>}
             OR
             schedule: [{group: [optional], type: [optional], every: 4, unit: "minutes/hours/days/weeks/months/years", actions: <<list of actions or name of sequence>>}
           returns : The ID of the sequence sent, returned from FarmBot

           This function turns a list of actions into a YAML sequence with a
           program-set name, then turns it into a CeleryScript command, sends
           it off and gets the ID back, and writes the YAML sequence object
           with its name and ID to internal storage."""

        str_obj = json.dumps(yaml_obj)
        needs_a_csv = ("group" in yaml_obj or "type" in yaml_obj or "to_plant" in str_obj or "to_self" in str_obj)
        child_needs_csv = False

        name = ""
        auto = 1 # not-zero is true
        id = -1

        hash = sha224(json.dumps(yaml_obj).encode()).hexdigest()

        if obj_name is not None:
            if needs_a_csv:
                name = obj_name + "_" + self.map
            else:
                name = obj_name
            changed, id = self.check_change(yaml_obj, name)
            if not changed:
                return (id, obj_name, False)
        else:
            name = stor.unique_name(hash)

        script = "{"

        script = script + "\n  \"color\": \"" + self.default(yaml_obj, "color", source_file) + "\","

        script = script + "\n  \"name\": \"" + name + "\","
        data = {name : {"auto": auto, "kind" : "regimen", "hash":hash, "children":[]}}
        # if needs_a_csv:
            # data["CSV"] = self.map
            # data["csv_hash"] = sha224((f.read()).encode()).hexdigest()

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
            seq_id = -1
            n = ""
            if type(sequence["actions"]) is not str:
                # If the actions in the regimen is a list,
                # and we need to generate the sequence ourselves.
                seq_id, n, this_needs_csv = self.make_sequence(send_this, source_file)
                child_needs_csv = (child_needs_csv or this_needs_csv)
            else:
                # If the actions refer to a sequence defined elsewhere by the user,
                # and we need to find it.
                looking_for = sequence["actions"]
                for file_name in self.source_files:
                    f = open(file_name, 'r')
                    file = yaml.load(f)
                    if looking_for in file:
                        send_this["actions"] = file[looking_for]["actions"]
                        # We don't include the sequence name because the regimen
                        # may have different groups and types, and therefore needs
                        # a new automatic sequence with the same actions.
                        # But we still need to add the user-defined child in case it changes later.
                        data[name]["children"].append(looking_for)
                        seq_id, n, this_needs_csv = self.make_sequence(send_this, source_file, obj_name=None)
                        child_needs_csv = (child_needs_csv or this_needs_csv)
                        f.close()
                        break
                    f.close()
                if (seq_id==-1):
                    raise Exception("The sequence "+looking_for+" required was not found.")
            data[name]["children"].append(n)
            list_of_sequences.append({"id":seq_id,"time_offsets": self.calc_time_offsets(sequence)})
            # Format all the sequences and their times for the regimen
        script = script + "\n  \"regimen_items\": [ "
        for sequence in list_of_sequences:
            time_offsets = sequence["time_offsets"]
            seq_id = sequence["id"]
            for offset in time_offsets:
                script = script + "\n    {"
                script = script + "\n      \"time_offset\": " + str(offset) + ","
                script = script + "\n      \"sequence_id\": " + str(seq_id)
                script = script + "\n    },"
        script = script[0:-1] # Truncate off the last comma of the last item
        # script = script + "\n  ], \n  \"uuid\": \""+name+"\"\n}"
        script = script + "\n  ]\n}"
        # script = json.dumps(json.loads(script), indent="  ", sort_keys=False)

        # If one of its children needs a CSV file
        # if not needs_a_csv and child_needs_csv:
            # data["CSV"] = self.map
            # data["csv_hash"] = sha224((f.read()).encode()).hexdigest()

        file = open("celeryscript.txt",'a')
        # file.write(json.dumps(json.loads(script), indent="  ", sort_keys=False))
        file.write(script)
        file.close()

        reg_id = http.new_command(json.loads(script), "regimen")
        data[name]["id"] = reg_id
        stor.add_data(data)

        return (reg_id, name, (needs_a_csv or child_needs_csv))

    def make_farm_event(self, yaml_obj, source_file, obj_name):
        """yaml_obj : An YAML object we already know is an event.
           returns : The ID of the event sent, returned from FarmBot

           This function turns a list of actions into a YAML event with a
           program-set name, then turns it into a CeleryScript command, sends
           it off and gets the ID back, and writes the YAML sequence object
           with its name and ID to internal storage."""


        str_obj = json.dumps(yaml_obj)
        needs_a_csv = ("group" in yaml_obj or "type" in yaml_obj or "to_plant" in str_obj or "to_self" in str_obj)
        child_needs_csv = False

        name = ""
        auto = 1 # not-zero is true
        id = -1
        hash = sha224(json.dumps(yaml_obj).encode()).hexdigest()

        if obj_name is not None:
            if needs_a_csv:
                name = obj_name + "_" + self.map
            else:
                name = obj_name
            changed, id = self.check_change(yaml_obj, name)
            if not changed:
                return (id, obj_name, False)
        else:
            name = stor.unique_name(hash)

        script = "{"

        data = {name : {"auto": 0, "kind" : "farm_event", "hash":hash, "children":[]}}

        # if needs_a_csv:
            # data["CSV"] = self.map
            # data["csv_hash"] = sha224((f.read()).encode()).hexdigest()

        script  = script + "\n  \"start_time\" : \"" + self.format_time(yaml_obj["start_time"]) + "\","
        if "repeat_event" in yaml_obj:
            # The following is a field in Farm Events:
            # repeat_event: {every: default 1, unit = "minutes/hours/days/weeks/months/years", until: ???}
            script = script + "\n  \"end_time\" : \"" + self.format_time(yaml_obj["repeat_event"]["until"]) + "\","
            script = script + "\n  \"repeat\" : " + self.default(yaml_obj["repeat_event"], "every", source_file) + ","
            script = script + "\n  \"time_unit\" : \"" + yaml_obj["repeat_event"]["unit"] + "\","
        else:
            script = script + "\n  \"time_unit\" : " + "\"never\","
            script = script + "\n  \"repeat\" : " + "1,"
        id = -1
        n = ""
        if "schedule" in yaml_obj:
            id, n, this_needs_csv = self.make_regimen({"schedule" : yaml_obj["schedule"]}, source_file)
            child_needs_csv = (child_needs_csv or this_needs_csv)
            script = script + "\n  \"executable_type\" : " + "\"Regimen\","
        elif "actions" in yaml_obj:
            if type(yaml_obj["actions"]) is not str:
                id, n, this_needs_csv = self.make_sequence({"actions" : yaml_obj["actions"]}, source_file)
                child_needs_csv = (child_needs_csv or this_needs_csv)
                script = script + "\n  \"executable_type\" : " + "\"Sequence\","
            else:
                id, kind, n, this_needs_csv = self.obj_from_name(yaml_obj["actions"])
                child_needs_csv = (child_needs_csv or this_needs_csv)
                script = script + "\n  \"executable_type\" : " + "\"" + kind + "\","
        script = script + "\n  \"executable_id\" : " + str(id) +  "\n }"
        data[name]["children"].append(n)

        file = open("celeryscript.txt",'a')
        file.write(script)
        file.close()

        event_id = http.new_command(json.loads(script),"farm_event")
        data[name]["id"] = event_id

        # If one of its children needs a CSV file
        # if not needs_a_csv and child_needs_csv:
            # data["CSV"] = self.map
            # data["csv_hash"] = sha224((f.read()).encode()).hexdigest()

        stor.add_data(data)

        return (id, name)
