import pandas as pd

    def origin_valu(value):
        data = pd.read_csv(path)
        x = data.x_coordinates
        y = data.y_coordinates 
        z = data.z_coordinates

    def excuted_value(regimen):
        if self.value != new_value:
            self.pre_change()
        else:
            self.post_change()

    def pre_change(self):
        # do stuff before variable is about to be changed
        print (False)
    def post_change(self):
        # do stuff right after variable has changed
        print (True)