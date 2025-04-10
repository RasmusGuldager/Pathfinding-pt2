from mazegenerator import mazegenerator
import random


def BFS(start, end):
    open_set = [start]
    closed_set = []

    while len(open_set) > 0:
        current = open_set.pop(0)

        closed_set.append(current)
        for neighbor in current.path_neighbors:
            if (
                neighbor not in closed_set
                and neighbor not in open_set
                and not neighbor.wall
            ):
                open_set.append(neighbor)
                neighbor.prev = current

        if current == end:
            # print("Path found!")
            path = mark_path(current)
            return path


def mark_path(current):
    path = [current]
    current = current.prev

    while current.prev is not None:
        path.append(current)
        current = current.prev

    path.append(current)
    
    path.reverse()

    return path


def main(config, height, width, start=None):
    grid = mazegenerator(config, height, width)

    if start is None:
        start = grid[0][random.randrange(1, len(grid[0]), 2)]
    else:
        start = grid[0][start.x]

    if height % 2 == 0:
        end = grid[height][random.randrange(1, len(grid[0]), 2)]
    else:
        end = grid[height - 1][random.randrange(1, len(grid[0]), 2)]

    start.wall = False
    end.wall = False

    start.icon = " "
    end.icon = " "

    if config["algorithms"]["path"] == "bfs":
        path = BFS(start, end)

    return grid, path, start, end
