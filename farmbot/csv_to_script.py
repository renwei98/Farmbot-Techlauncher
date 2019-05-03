import pandas as pd

def csv_to_celeryscript(path):
    content = pd.read_csv(path)
    script = "{"
    n = 0
    while n <= len(content)-1:
        script = script + "\n  \"name\" : \"" + (str(content["name"][n])) + "\","
        script = script + "\n  \"type\" : \"" + (str(content["type"][n])) + "\","
        script = script + "\n  \"group\" : \"" + (str(content["group"][n])) + "\","
        script = script + "\n  \"x\" : \"" + (str(content["x"][n])) + "\","
        script = script + "\n  \"y\" : \"" + (str(content["y"][n])) + "\","
        script = script + "\n  \"z\" : \"" + (str(content["z"][n])) + "\",\n"
        n+=1
    script = script + "}"
    print(script)
    return
