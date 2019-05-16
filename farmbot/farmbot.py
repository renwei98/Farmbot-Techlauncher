import argparse
import read_commands
import handle_internal_storage as stor
import util.api_token_gen as token_gen

parser = argparse.ArgumentParser()
parser.add_argument("-y","--yaml_files", type=str,
                    help="YAML files containing commands for the FarmBot, comma separated with NO spaces.")
parser.add_argument("-m","--map", type=str, default=None,
                    help="a single CSV file containing the map of plant locations.")
parser.add_argument("-d","--delete", type=str,
                    help="a) 'all', or b) a list of commands to delete, comma separated with NO spaces.")
parser.add_argument("-i","--login", type=str, nargs=2,
                    help="Login to your FarmBot using your existing account. If this option is not chosen, the program will assume you are still logged in from last time.")
parser.add_argument("-o","--logout", type=str,
                    help="Logout the Farmbot WebApp.")

args = parser.parse_args()
# remember to change 'myFile' to the name of User Manual
# parser.add_argument("-h", "--help", dest="myFile", help="open user manual")

# myFile = args.myFile
# text = open(myFile)
# print(text.read())

if args.login:
    token = token_gen.get_token(args.new_user[0], args.new_user[1])

    # login with new username and password -> generate a new .env file
    file = open(".env", "w+")
    file.write("EMAIL=\"" + args.new_user[0] + "\"\n")
    file.write("PASSWORD=\"" + args.new_user[1] + "\"\n")
    file.write("TOKEN=\"" + token + "\"\n")
    file.close()
if args.logout:
    # delete the content of .env file
    file = open(".env", "r+")
    file.truncate(0)


if args.delete:
    print("not here")
    if args.delete == "all":
        stor.delete_all()
    else:
        objects = args.delete.split(',')
        for obj in objects:
            stor.delete_object(obj)
if args.yaml_files:
    action_handler = read_commands.ActionHandler(args.yaml_files.split(','), args.map)
    print(action_handler.load_commands())
