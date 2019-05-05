import argparse
import read_commands

parser = argparse.ArguementParser()
parser.add_arguement("yaml_files", type=str,
 help="YAML files containing commands for the FarmBot, comma separated with NO spaces.")
parser.add_arguement("-m","--map", type=str, default=None,
 help="a single CSV file containing the map of plant locations.")
parser.add_arguement("-d","--defaults", type=str, default=None,
 help="a single YAML file specifying the default settings.")

args = parser.parse_args()

action_handler = ActionHandler(args.yaml_files.split(','), args.defaults, args.map)
print(action_handler.format_time("21/12/2019 23:00"))
