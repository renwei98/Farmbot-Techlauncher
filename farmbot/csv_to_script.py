import pandas as pd

def csv_to_celeryscript(path):
    content = pd.read_csv(path)
    n = 0
    script = ""
    while n <= len(content):
        
        
        script = script + "\n  \"plant_type\" : \"" + content["plant_type"][n] + "\","
        script = script + "\n  \"group_number\" : " + content["group_number"][n] + "\","
        script = script + "\n  \"x_coordinates\" : \"" + content["x_coordinates"][n] + "\","
        script = script + "\n  \"y_coordinates\" : \"" + content["y_coordinates"][n] + "\","
        script = script + "\n  \"z_coordinates\" : " + content["z_coordinates"][n] + "\","
        script = script + "\n  \"init_plant_date\" : \"" + content["init_plant_date"][n] + "\","
        n += 1
        
    return script
