import pandas as pd


def csv_to_script():
    content = pd.read_csv('../data/test.csv')
    
    #same group same type
    def is_missing(type, group):
        if pd.isnull(type):
            return content.loc[content['group'] == group, 'type']
        else:
            return type
    content['type'] = content.apply(lambda x : is_missing(x['type'], x['group']), axis = 1)
    
    content['name'] = content['name'].fillna('default_plant')
    content['type'] = content['type'].fillna('default_type')
    content['group'] = content['group'].fillna('default_group')
    content['x'] = content['x'].fillna(str(0))
    content['y'] = content['y'].fillna(str(0))
    content['z'] = content['z'].fillna(str(0))
        
    script = ""
    n = 0
    while n <= len(content)-1:
        script = script + "{\"name\" : \"" + (str(content["name"][n])) + "\","
        script = script + "\"x\" : \"" + (str(content["x"][n])) + "\","
        script = script + "\"y\" : \"" + (str(content["y"][n])) + "\","
        script = script + "\"z\" : \"" + (str(content["z"][n])) + "\","
        script = script + "\"pointer_type\" : \"" + (str(content["type"][n])) + "\"}"
    
        n+=1
    return script
