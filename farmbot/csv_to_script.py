import pandas as pd
import json

<<<<<<< HEAD
content = pd.read_csv("test.csv")

print(content)
=======
def csv_to_celeryscript(path):
    content = pd.read_csv(path)
    script = content.to_dict(orient="records")
    script = str(script)
    script = script.replace("[","")
    script = script.replace("]","")
    script = script.replace("'",'"')
    
    json.dumps(script)
    return script
>>>>>>> 7ab9c84d6e69d9ea55e6bf5d204f9d24729d90e4
