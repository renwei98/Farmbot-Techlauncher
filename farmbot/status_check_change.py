class FarmBot:
    """ A simple class, set to watch its variable. """
    def init(self, value):
        self.variable = value

    def set_value(self, new_value):
        if self.value != new_value:
            self.pre_change()
            self.variable = new_value
            self.post_change()

    def pre_change(self):
        # do stuff before variable is about to be changed
        print (False)
    def post_change(self):
        # do stuff right after variable has changed
        print (True)