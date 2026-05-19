from .constants import RED, YELLOW

class Counter:
    def __init__(self):
        self.red_count = 0
        self.yellow_count = 0
    
    def increase(self, color):
        if color == YELLOW:
            self.yellow_count += 1
        elif color == RED:
            self.red_count += 1
        
    def return_red_count(self):
        return self.red_count

    def return_yellow_count(self):
        return self.yellow_count
    