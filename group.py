import numpy as np


class Group:
    def __init__(self, pocket_id, label_map):
        self.id = pocket_id
        self.coords = np.argwhere(label_map == pocket_id)
        self.size = len(self.coords)
        self.center = self.coords.mean(axis=0).astype(int)

