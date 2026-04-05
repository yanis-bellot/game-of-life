import numpy as np


class Group:

    def __init__(self, pocket_id, label_map, grid):
        self.grid = grid.value
        self.id = pocket_id
        self.label_map = label_map
        self.coords = np.argwhere(label_map == pocket_id)
        self.size = len(self.coords)
        self.center = self.coords.mean(axis=0).astype(int)
        self.interior = np.roll(self.coords, 1, axis=0) & np.roll(self.coords, -1, axis=0) & np.roll(self.coords, 1, axis=1) & np.roll(self.coords, -1, axis=1)
        self.border = self.coords & ~self.interior

    def get_coord(self, coord):
        if coord in self.coords:
            return self.center
        else:
            return None


    def get_minimal_link_BFS(self, selected_group):
        def BFS():
            dists = np.full(self.grid.shape, -1, dtype=np.int32)
            dists[self.coords] = 0
            current_dist = 0
            found_pos = None
            adj = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
            while True:
                y_coords, x_coords = np.where(distances == current_dist)
                if len(y_coords) == 0:
                    break

                next_dist = current_dist + 1

                for dy, dx in adj:
                    ny, nx = y_coords + dy, x_coords + dx

                    mask = (ny >= 0) & (ny < self.grid.shape[0]) & (nx >= 0) & (nx < self.grid.shape[1])

                    ny, nx = ny[mask], nx[mask]
                    unvisited = (dists[ny, nx] == -1)
                    ny, nx = ny[unvisited], nx[unvisited]

                    if len(ny) > 0:
                        dists[ny, nx] = next_dist
                        target_mask = (self.label_map[ny, nx] == selected_group.id)
                        if np.any(target_mask):
                            idx = np.where(target_mask)[0][0]
                            found_pos = (ny[idx], nx[idx])
                            break

                if found_pos:
                    break
                current_dist += 1
            return dists, found_pos

        distances, found_pos = BFS()
        path = [selected_group.center]
        curr_y, curr_x = selected_group.center

        while distances[curr_y, curr_x] > 0:
            d = distances[curr_y, curr_x]
            adj = [(0, 1), (0, -1), (1, 0), (-1, 0)]

            for dy, dx in adj:
                ny, nx = curr_y + dy, curr_x + dx
                if 0 <= ny < distances.shape[0] and 0 <= nx < distances.shape[1]:
                    if distances[ny, nx] == d - 1:
                        curr_y, curr_x = ny, nx
                        path.append((curr_y, curr_x))
                        break
        return path

