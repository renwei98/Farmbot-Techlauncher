import pandas as pd
import json


content = pd.read_csv("test.csv")

print(content)

def csv_to_celeryscript(path):
    content = pd.read_csv(path)
    script = content.to_dict(orient="records")
    script = str(script)
    script = script.replace("[","")
    script = script.replace("]","")
    script = script.replace("'",'"')
    
    json.dumps(script)
    return script

