import yaml

file_contents = yaml.safe_load(open("../data/test_yaml.yaml"))
print(file_contents)

# TODO Might be easier to split into lexer and parser, or convert to object then object to celeryscript


def move(move_type: str):  # Parsing function to generate celeryscript for moving absolute or relative
    return ""


# read events/sequences/regimens
for name in file_contents:
    if name == 'options':
        continue  # read options here

    if file_contents[name]['event_type'] == 'event':  # should check if event_type exists for safety
        pass
        # do event parsing
    elif file_contents[name]['event_type'] == 'regimen':
        pass
        # do regimen parsing
    elif file_contents[name]['event_type'] == 'sequence':
        # do sequence parsing
        print(file_contents[name])
        if 'colour' in file_contents[name]:
            pass

        if 'actions' in file_contents[name]:
            print(file_contents[name]['actions'])
            if 'MOVE_REL' in file_contents[name]['actions'][0]:  # Too many arguments on file_contents
                movement_script = move('RELATIVE')

        color = ""
        body = ""
        celery = "{'name': '" + name + "', 'color': " + color + " 'body':" + body + "}"
        print(celery)
