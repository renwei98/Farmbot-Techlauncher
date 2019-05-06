import argparse
import read_commands

parser = argparse.ArgumentParser()
parser.add_argument("-y","--yaml_files", type=str,
                    help="YAML files containing commands for the FarmBot, comma separated with NO spaces.")
parser.add_argument("-m","--map", type=str, default=None,
                    help="a single CSV file containing the map of plant locations.")
parser.add_argument("-d","--delete", type=str,
                    help="a) 'all', or b) a list of commands to delete, comma separated with NO spaces.")

args = parser.parse_args()

if args.delete:
    if args.delete == "all":
        stor.delete_all()
    else:
        objects = args.delete.split(',')
        for obj in objects:
            stor.delete_object(obj)
if args.yaml_files:
    action_handler = read_commands.ActionHandler(args.yaml_files.split(','), args.map)
# print(action_handler.source_files)
# print(action_handler.calc_time_offsets({"group": ["extra_water_group"], "type": ["radish"], "days": [1,2,3], "times": ["23:00", "12:00"], "actions": "move_farmbot_2"}))
# print(action_handler.calc_time_offsets({"every": 4, "unit": "months", "max": 10}))
# print(action_handler.parse_coord(coords={"x_off":9}, source_file="test_yaml.yaml"))
