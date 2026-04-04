class Field:

    #size :: [x :: int ,y :: int] , rules :: [living threshold :: [int; int...9] , dying map :: [int, int...9]]
    def __init__(self, size, rules):
        self.name = "Field of play"
        self.value = [[0 for i in range(size[0])] for j in range(size[1])]
        self.rules = rules
        self.gen_count = 0


    def is_alive(self, field, x, y):
        if 0 <= x < len(self.value[0]) and 0 <= y < len(self.value):
            if field[y][x] == 0:
                return False
            else:
                return True
        else:
            return False


    def check_alive_neighbors(self, field, x, y):
        alive_neighbors = 0
        directions = [(0, -1),(0, 1),(-1, 0),(1, 0), (1, 1), (1,-1), (-1, 1), (-1, -1)]
        for dx, dy in directions:
            neighbor_x, neighbor_y = x + dx, y + dy
            if self.is_alive(field, neighbor_x, neighbor_y):
                alive_neighbors += 1
        return alive_neighbors


    def refresh(self):
        value_before = self.value
        for y in range(len(value_before)):
            for x in range(len(value_before[y])):
                if self.is_alive(value_before, x, y):
                    value_before[y][x] = self.rules[1][self.check_alive_neighbors(value_before, x, y)]
                else:
                    value_before[y][x] = self.rules[0][self.check_alive_neighbors(value_before, x, y)]

        self.value = value_before
        self.gen_count += 1
        return self.value
