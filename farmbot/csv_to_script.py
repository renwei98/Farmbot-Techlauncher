import pandas as pd
import json

def csv_to_celeryscript(path):
    content = pd.read_csv(path)
    script = "{"
    n = 0
    while n <= len(content)-1:
        script = script + "\n  \"plant_type\" : \"" + content["plant_type"][n] + "\","
        script = script + "\n  \"group_number\" : \"" + (str(content["group_number"][n])) + "\","
        script = script + "\n  \"x_coordinates\" : \"" + (str(content["x_coordinates"][n])) + "\","
        script = script + "\n  \"y_coordinates\" : \"" + (str(content["y_coordinate"][n])) + "\","
        script = script + "\n  \"z_coordinates\" : \"" + (str(content["z_coordinate"][n])) + "\","
        script = script + "\n  \"init_plant_date\" : \"" + (str(content["init_plant_date"][n])) + "\",\n"
        n+=1
    script = script + "}"
    print(script)
    return