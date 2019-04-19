import pandas as pd
    data = pd.read_csv(path)
    x = data.x_coordinates
    y = data.y_coordinates 
    z = data.z_coordinates

    def excuted_value(regimen):
        for elemx in x:
            if elemx != new_value:
            self.pre_change()
            else:
            self.post_change()
        for elemy in y:
            if elemy != new_value:
            self.pre_change()
            else:
            self.post_change()
        for elemz in z:
            if elemz != new_value:
            self.pre_change()
            else:
            self.post_change()
    def pre_change(self):
        print (False)
    def post_change(self):
        print (True)