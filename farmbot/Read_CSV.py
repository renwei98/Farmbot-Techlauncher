""" Rachel: I think the most important part is that this class should, like
 read_sequence and read_regimen
  - Be able to return CeleryScript that can be sent to FarmBot
  - Provide a function that writes what FarmBot returns back to the CSV
     * (e.g. in read_commands, update_sequence(self, seq_name, returned_id)
             writes the returned ID back to the YAML file) """

class MapHandler():
    def __init__(self):
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

        # Parse lines by the headings of lines
        for line in lines_list:
            if line != lines_list[0]:
                plant_type = line[0]
                group_number = line[1]
                x_coordinate = line[2]
                y_coordinate = line[3]
                z_coordinate = line[4]
                init_plant_date = line[5]
        # save variables in current instance of class
        self.plant_type = plant_type
        self.group_number = group_number
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.z_coordinate = z_coordinate
        self.init_plant_date = init_plant_date
