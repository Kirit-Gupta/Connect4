class Cell:
    def __init__(self):
        self.fill = False
        self.color = None
    
    def is_empty(self):
        return not self.fill

    def add_counter(self, counter_color):
        self.color = counter_color
        self.fill = True
    
    def get_color(self):
        if not self.is_empty():
            return self.color