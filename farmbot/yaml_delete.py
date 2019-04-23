
import yaml

def yaml_delete_object(file_name, object_id):
    with open(file_name, 'r') as stream:
        try:
            file = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    
    for elem in file:
        if elem["id"] == object_id:
            elem["regimen_items"] = []
             
    with open(file_name, "w") as stream:
        yaml.dump(file, stream)

            
    
