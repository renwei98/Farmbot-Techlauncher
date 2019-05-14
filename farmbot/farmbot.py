import argparse
import read_commands
import csv

parser = argparse.ArgumentParser()
parser.add_argument("-y","--yaml_files", type=str,
                    help="YAML files containing commands for the FarmBot, comma separated with NO spaces.")
parser.add_argument("-m","--map", type=str, default=None,
                    help="a single CSV file containing the map of plant locations.")
parser.add_argument("-d","--delete", type=str,
                    help="a) 'all', or b) a list of commands to delete, comma separated with NO spaces.")
parser.add_argument("-i","--login", type=str,
                    help="Login the Farmbot WebApp by email as username and password.")
parser.add_argument("-n","--new_account", type=str,
                    help="Register your new account for FarmBot.")
parser.add_argument("-o","--logout", type=str,
                    help="Logout the Farmbot WebApp.")

args = parser.parse_args()
#remember to change 'myFile' to the name of User Manual
# parser.add_argument("-h", "--help", dest="myFile", help="open user manual")
args = parser.parse_args()
# myFile = args.myFile
# text = open(myFile)
# print(text.read())

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
if args.login:
    # login with crendentials from .env file
    success = False;
    username_input = input("Welcome to FarmBot! \n\n Please Enter your Username: ");
    if username_input == os.getenv("EMAIL"):
        password_input = input("please Enter your Password: ");
        if password_input == os.getenv("PASSWORD"):
                success = True;
                print("Your login is successful!");
        else:
            print("Your Password is invalid");
    else:
        print("Your Username is invalid");
    
    if success == False:
        print("Could you try another attempt? Please type --i");
        print("or You may create a new account for Farmbot! Please type --n");
if args.new_account:
    # login with new username and password -> generate a new .env file
    file = open(".env", "w+");
    username_input = input("Please Enter your Email Address for new Acccount: ");
    os.environ("EMAIL") = username_input;
    password_input = input("Please Enter your Password for your new Account: ");
    os.environ("PASSWORD") = password_input;
    file.write(os.environ("EMAIL"), os.environ("PASSWORD"));
    file.close();
    print("Successful! You have registered a new Account!");
    print("Please login your Account by Typing --i")
if args.logout:
        # delete the content of .env file
        file = open(".env", "r+");
        file.truncate(0);
    
if False:
    print(action_handler.map)
    print(action_handler.parse_action(action={"move_rel": {"x": 10, "y": 10, "z": 10, "speed": 10, "x_off": 10, "y_off": 9, "z_off": 8}}, source_file="../data/test_yaml.yaml"))
    print(action_handler.parse_action(action={"move_abs": {"x": 0, "y": 0}}, source_file="../data/test_yaml.yaml"))
    with open("../data/test.csv", "r") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            print(action_handler.parse_action(action={"to_self":{"x_off":10}}, row=row, source_file="../data/test_yaml.yaml"))
    print(action_handler.parse_action(action={"find_home": ["x","y"]}, source_file="../data/test_yaml.yaml"))
    print(action_handler.parse_action(action={"wait": 1000}, source_file="../data/test_yaml.yaml"))
    print(action_handler.parse_action(action={"read_pin": {"pin": "water_pin", "label": "variable", "mode":"D"}}, source_file="../data/test_yaml.yaml"))
    print(action_handler.parse_action(action={"write_pin": {"pin": "water_pin", "value": "ON", "mode":"D"}}, source_file="../data/test_yaml.yaml"))
    print(action_handler.parse_action(action={"to_plant": {"name":"plant2","x_off":0, "speed":60}}, source_file="../data/test_yaml.yaml"))


# print(action_handler.source_files)
# print(action_handler.calc_time_offsets({"group": ["extra_water_group"], "type": ["radish"], "days": [1,2,3], "times": ["23:00", "12:00"], "actions": "move_farmbot_2"}))
# print(action_handler.calc_time_offsets({"every": 4, "unit": "months", "max": 10}))
# print(action_handler.parse_coord(coords={"x_off":9}, source_file="../data/test_yaml.yaml"))
