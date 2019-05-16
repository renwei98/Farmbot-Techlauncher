import argparse
import read_commands
import csv
import handle_internal_storage as stor

parser = argparse.ArgumentParser()
parser.add_argument("-y","--yaml_files", type=str,
                    help="YAML files containing commands for the FarmBot, comma separated with NO spaces.")
parser.add_argument("-m","--map", type=str, default=None,
                    help="a single CSV file containing the map of plant locations.")
parser.add_argument("-d","--delete", type=str,
                    help="a) 'all', or b) a list of commands to delete, comma separated with NO spaces.")
parser.add_argument("-i","--login", type=str,
                    help="Login to your FarmBot using your existing account. If this option is not chosen, the program will assume you are still logged in from last time.")
parser.add_argument("-o","--logout", type=str,
                    help="Logout the Farmbot WebApp.")

args = parser.parse_args()
# remember to change 'myFile' to the name of User Manual
# parser.add_argument("-h", "--help", dest="myFile", help="open user manual")
args = parser.parse_args()
# myFile = args.myFile
# text = open(myFile)
# print(text.read())

if args.login:
    # login with new username and password -> generate a new .env file
    file = open(".env", "w+");
    username_input = input("Enter email address: ");
    os.environ("EMAIL") = username_input;
    password_input = input("Enter password: ");
    os.environ("PASSWORD") = password_input;
    file.write(os.environ("EMAIL"));
    file.write(os.environ("PASSWORD"));
    file.close();
if args.logout:
    # delete the content of .env file
    file = open(".env", "r+");
    file.truncate(0);


if args.delete:
    if args.delete == "all":
        stor.delete_all()
    else:
        objects = args.delete.split(',')
        for obj in objects:
            stor.delete_object(obj)
if args.yaml_files:
    action_handler = read_commands.ActionHandler(args.yaml_files.split(','), args.map)
    print(action_handler.load_commands())
