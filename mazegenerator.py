import random
from convert_ascii import convert_ascii


class Spot:
    def __init__(self, y, x):
        self.x = x
        self.y = y
        self.wall = True
        self.maze_neighbors = []
        self.path_neighbors = []
        self.icon = "#"
        self.color_code = None
        self.prev = None
    
    def __hash__(self):
        return hash((self.x, self.y))
    
    def __eq__(self, other):
        return isinstance(other, Spot) and self.x == other.x and self.y == other.y

    def find_maze_neighbors(self, grid):
        if self.x > 2:
            self.maze_neighbors.append(grid[self.y][self.x - 2])
        if self.x < len(grid[0]) - 3:
            self.maze_neighbors.append(grid[self.y][self.x + 2])
        if self.y > 2:
            self.maze_neighbors.append(grid[self.y - 2][self.x])
        if self.y < len(grid) - 3:
            self.maze_neighbors.append(grid[self.y + 2][self.x])

    def find_path_neighbors(self, grid):
        if self.x > 0:
            self.path_neighbors.append(grid[self.y][self.x - 1])
        if self.x < len(grid[0]) - 1:
            self.path_neighbors.append(grid[self.y][self.x + 1])
        if self.y > 0:
            self.path_neighbors.append(grid[self.y - 1][self.x])
        if self.y < len(grid) - 1:
            self.path_neighbors.append(grid[self.y + 1][self.x])


def generate_grid(width, height):
    grid = [[0 for _ in range(width)] for _ in range(height)]

    for y in range(height):
        for x in range(width):
            grid[y][x] = Spot(y, x)

    for y in range(height):
        for x in range(width):
            grid[y][x].find_maze_neighbors(grid)
            grid[y][x].find_path_neighbors(grid)

    return grid


def prims_generate_maze(grid):
    row = random.randrange(1, len(grid), 2)
    col = random.randrange(1, len(grid[0]), 2)

    start = grid[row][col]

    start.wall = False
    start.icon = " "

    open_set = []
    closed_set = [start]

    for neighbor in start.maze_neighbors:
        open_set.append(neighbor)

    while len(open_set) > 0:
        current = random.choice(open_set)
        open_set.remove(current)
        closed_set.append(current)
        current.wall = False
        current.icon = " "
        current_neighbors = []

        for neighbor in current.maze_neighbors:
            if neighbor.wall and neighbor not in open_set and neighbor:
                open_set.append(neighbor)

            elif neighbor in closed_set:
                current_neighbors.append(neighbor)

        chosen_connection = random.choice(current_neighbors)

        path_x = (current.x + chosen_connection.x) // 2
        path_y = (current.y + chosen_connection.y) // 2

        grid[path_y][path_x].wall = False
        grid[path_y][path_x].icon = " "

    #print("Generated maze!")
    return grid


def dfs_generate_maze(grid):
    row = random.randrange(1, len(grid), 2)
    col = random.randrange(1, len(grid[0]), 2)

    start = grid[row][col]

    start.wall = False
    start.icon = " "

    open_set = [start]
    current = start
    current_neighbors = []

    while len(open_set) > 0:

        current.wall = False
        current.icon = " "

        for neighbor in current.maze_neighbors:
            if neighbor.wall:
                current_neighbors.append(neighbor)

        if len(current_neighbors) == 0:
            current = open_set.pop()

        else:
            chosen_connection = random.choice(current_neighbors)

            path_x = (current.x + chosen_connection.x) // 2
            path_y = (current.y + chosen_connection.y) // 2

            grid[path_y][path_x].wall = False
            grid[path_y][path_x].icon = " "

            current = chosen_connection
            open_set.append(current)

        current_neighbors = []

    #print("Generated maze!")
    return grid


def mazegenerator(config, height, width):
    if width < 3 or height < 3:
        raise ValueError("Width and height must be at least 3.")

    width += width % 2 == 0
    height += height % 2 == 0

    grid = generate_grid(width, height)

    if config['algorithms']['maze'] == "prims":
        prims_generate_maze(grid)
    elif config['algorithms']['maze'] == "dfs":
        dfs_generate_maze(grid)

    grid = convert_ascii(config, grid, "wall")

    return grid


if __name__ == "__main__":
    mazegenerator(121, 19)