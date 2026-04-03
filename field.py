class Field:

    #size :: [x :: int ,y :: int] , rules :: [living threshold :: int , dying threshold :: [int, int...]]
    def __init__(self, size, rules):
        self.name = "Field of play"
        self.value = [[0 for i in range(size[0])] for j in range(size[1])]
        self.rules = rules

    def refresh(self):
        for lines in self.value:
            for i in range(len(lines)):
                pass


    def is_alive(self, x, y):
        if self.value[y][x] == 0:
            return False
        else:
            return True


    def check_neighbors_alive(self, x, y):
        alive_neighbors = 0


    def check_neighbors(self, x, y):
        if self.is_alive(x, y):
            pass
