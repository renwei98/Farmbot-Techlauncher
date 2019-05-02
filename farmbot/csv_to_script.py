import pandas as pd

content = pd.read_csv(path)
script = ""
script1 = script + "\n  \"plant_type\" : \"" + content["plant_type"][n] + "\","
script2 = script + "\n  \"group_number\" : \"" + (str(content["group_number"][n])) + "\","
script3 = script + "\n  \"x_coordinates\" : \"" + (str(content["x_coordinates"][n])) + "\","
script4 = script + "\n  \"y_coordinates\" : \"" + (str(content["y_coordinate"][n])) + "\","
script5 = script + "\n  \"z_coordinates\" : \"" + (str(content["z_coordinate"][n])) + "\","
script6 = script + "\n  \"init_plant_date\" : \"" + (str(content["init_plant_date"][n])) + "\","
print("{", script1, script2, script3, script4, script5, script6,"\n}")
        