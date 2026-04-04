class Field:

    #size :: [x :: int ,y :: int] , rules :: [living threshold :: [int; int...9] , dying map :: [int, int...9]]
    def __init__(self, size, rules):
        self.name = "Field of play"
        self.value = [[0 for i in range(size[0])] for j in range(size[1])]
        self.rules = rules
        self.gen_count = 0

    def reset(self):
        self.value = [[0 for i in range(len(self.value[0]))] for j in range(len(self.value))]
        self.gen_count = 0

    def is_alive(self, x, y):
        if 0 <= x < len(self.value[0]) and 0 <= y < len(self.value):
            if self.value[y][x] == 0:
                return False
            else:
                return True
        else:
            return False


    def check_alive_neighbors(self, x, y):
        alive_neighbors = 0
        directions = [(0, -1),(0, 1),(-1, 0),(1, 0), (1, 1), (1,-1), (-1, 1), (-1, -1)]
        for dx, dy in directions:
            neighbor_x, neighbor_y = x + dx, y + dy
            if self.is_alive(neighbor_x, neighbor_y):
                alive_neighbors += 1
        return alive_neighbors


    def refresh(self):
        new_value = [[0 for i in range(len(self.value[0]))] for j in range(len(self.value))]
        for y in range(len(self.value)):
            for x in range(len(self.value[y])):
                if self.is_alive(x, y):
                    new_value[y][x] = self.rules[1][self.check_alive_neighbors(x, y)]
                else:
                    new_value[y][x] = self.rules[0][self.check_alive_neighbors(x, y)]

        self.value = new_value
        self.gen_count += 1
        return self.value
