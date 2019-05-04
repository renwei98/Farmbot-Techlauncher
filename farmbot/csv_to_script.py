import pandas as pd
import numpy as np

content = pd.read_csv('../data/test.csv')

def is_missing(type, group):
    if pd.isnull(type):
        return content.loc[content['group'] == group, 'type']
    else:
        return type
content['type'] = content.apply(lambda x : is_missing(x['type'], x['group']), axis = 1)

"""content['name'] = content['name'].fillna('plant')
content['type'] = content['type'].fillna('extra_water_group')
content['group'] = content['group'].fillna('radish')
content['x'] = content['x'].fillna(str(0))
content['y'] = content['y'].fillna(str(0))
content['z'] = content['z'].fillna(str(0))"""
    
script = ""
n = 0
while n <= len(content)-1:
    script = script + "{\"name\" : \"" + (str(content["name"][n])) + "\","
    script = script + "\"x\" : \"" + (str(content["x"][n])) + "\","
    script = script + "\"y\" : \"" + (str(content["y"][n])) + "\","
    script = script + "\"z\" : \"" + (str(content["z"][n])) + "\","
    script = script + "\"pointer_type\" : \"" + (str(content["type"][n])) + "\"}"

    n+=1
display(content)
print(script)
