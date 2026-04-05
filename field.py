import numpy as np
import scipy


class Field:

    #size :: [x :: int ,y :: int] , rules :: [living threshold :: [int; int...9] , dying map :: [int, int...9]]
    def __init__(self, size, rules):
        self.value = np.zeros((size[1], size[0]), dtype=np.int8)
        self.rules = [np.array(r, dtype=np.int8) for r in rules]
        self.gen_count = 0

    def reset(self):
        self.value.fill(0)
        self.gen_count = 0

    def refresh(self):
        nbrs = np.zeros_like(self.value)
        nbrs[1:-1, 1:-1] = (
                self.value[:-2, :-2] + self.value[:-2, 1:-1] + self.value[:-2, 2:] +
                self.value[1:-1, :-2] + self.value[1:-1, 2:] +
                self.value[2:, :-2] + self.value[2:, 1:-1] + self.value[2:, 2:]
        )
        is_alive = (self.value == 1)
        is_dead = (self.value == 0)

        new_value = np.zeros_like(self.value)

        new_value[is_dead] = self.rules[0][nbrs[is_dead]]
        new_value[is_alive] = self.rules[1][nbrs[is_alive]]

        self.value = new_value
        self.gen_count += 1

    def get_pockets(self):
        dead_mask = (self.value == 0)
        structure = np.ones((3, 3), dtype=int)
        label_map, num_pockets = label(dead_mask, structure=structure)
        return label_map, num_pockets