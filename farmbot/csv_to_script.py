import pandas as pd


content = pd.read_csv('test.csv')

content['name'] = content['name'].fillna('plant')
content['type'] = content['type'].fillna('extra_water_group')
content['group'] = content['group'].fillna('radish')
content['x'] = content['x'].fillna(str(0))
content['y'] = content['y'].fillna(str(0))
content['z'] = content['z'].fillna(str(0))
    
script = "{"
n = 0
while n <= len(content)-1:
    script = script + "\"name\" : \"" + (str(content["name"][n])) + "\","
    script = script + "\"type\" : \"" + (str(content["type"][n])) + "\","
    script = script + "\"group\" : \"" + (str(content["group"][n])) + "\","
    script = script + "\"x\" : \"" + (str(content["x"][n])) + "\","
    script = script + "\"y\" : \"" + (str(content["y"][n])) + "\","
    script = script + "\"z\" : \"" + (str(content["z"][n])) + "\","
    n+=1
script = script + "}"
    
