""" Rachel: I think the most important part is that this class should, like
 read_sequence and read_regimen
  - Be able to return CeleryScript that can be sent to FarmBot
  - Provide a function that writes what FarmBot returns back to the CSV
     * (e.g. in read_commands, update_sequence(self, seq_name, returned_id)
             writes the returned ID back to the YAML file) """
from tempfile import NamedTemporaryFile
import shutil
import csv

class MapHandler():
    def __init__(self):
        self.plant_id = ""
        self.plant_type = ""
        self.group_number = 0
        self.x_coordinate = 0.0
        self.y_coordinate = 0.0
        self.z_coordinate = 0.0
        self.init_plant_date = (0, 0, 0)


    def read_csv(self, path_file):
        file = open(path_file, "r")
        content = file.read()
        # Parse content by lines
        lines_list = content.splitlines()
        # Parse lines by whitespace delimiter
        for line in lines_list:
            line.split()
          
        # Set the lines_list[0] as the keys of dictionary
        attribute_list = lines_list[0].split()
        my_dict = dict((el:"") for el in attribute_list)
        # Parse lines by the headings of lines
        for line in lines_list:
            if line != lines_list[0]:
                plant_id = line[0]
                plant_type = line[1]
                group_number = line[2]
                x_coordinate = line[3]
                y_coordinate = line[4]
                z_coordinate = line[5]
                init_plant_date = line[5]
        # save variables in current instance of class
        self.plant_id = plant_id
        self.plant_type = plant_type
        self.group_number = group_number
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.z_coordinate = z_coordinate
        self.init_plant_date = init_plant_date
    
    # not sure the flow of updation, completed after get rid of confusion
    def update_to_csv():
        filename = 'my.csv'
        tempfile = NamedTemporaryFile(mode='w', delete=False)

        fields = ['plant_id', 'plant_type', 'group_number', 
                  'x_coordinate', 'y_coordinate', 'z_coordinate',
                 'init_plant_date']

        with open(filename, 'r') as csvfile, tempfile:
             reader = csv.DictReader(csvfile, fieldnames=fields)
             writer = csv.DictWriter(tempfile, fieldnames=fields)
             for row in reader:
                 if row['plant_id'] == str(plant_id):
                    row['plant_type'] = plant_type
                    row['group_number'] = group_number
                    row['x_coordinate'] = x_coordinate
                    row['y_coordinate'] = y_coordinate
                    row['z_coordinate'] = z_coordinate
                    row['init_plant_date'] = init_plant_date
                 row = {'plant_id': row['plant_id'], 'plant_type': row['plant_type'], 
                           'group_number': row['group_number'], 'x_coordinate': row['x_coordinate'],
                           'y_coordinate': row['y_coordinate'],'z_coordinate': row['z_coordinate'],
                           'init_plant_date': row['init_plant_date']}
                 writer.writerow(row)

     shutil.move(tempfile.name, filename)
     
