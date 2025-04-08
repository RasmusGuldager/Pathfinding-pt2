from mazegenerator import mazegenerator
from print_to_file import print_grid_to_file
from convert_ascii import convert_ascii
import math, random


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
            #print("Path found!")
            path = mark_path(current)
            return path


def mark_path(current):
    path = [current]
    current = current.prev
    count = 0

    while current.prev is not None:
        path.append(current)
        current.color = rainbow_256(count)[0]
        count += 1
        current = current.prev

    path.append(current)
    path.reverse()

    return path


def rainbow_256(i, freq=0.1):
    # These formulas produce smooth transitions
    r = math.sin(freq * i + 0) * 127 + 128
    g = math.sin(freq * i + 2 * math.pi / 3) * 127 + 128
    b = math.sin(freq * i + 4 * math.pi / 3) * 127 + 128

    # Map to xterm 256-color cube
    r_code = int(r * 6 / 256)
    g_code = int(g * 6 / 256)
    b_code = int(b * 6 / 256)

    color_code = 16 + 36 * r_code + 6 * g_code + b_code
    return f"\033[38;5;{color_code}m", color_code


def main(config, height, width, start=None, print_path=False):
    grid = mazegenerator(config, height, width)

    if not start:
        start = grid[0][random.randrange(1, len(grid[0]), 2)]
    else:
        start = grid[0][start.x]

    if height % 2 == 0:
        end = grid[height][random.randrange(1, len(grid[0]), 2)]
    else:
        end = grid[height - 1][random.randrange(1, len(grid[0]), 2)]
        
    start.wall = False
    end.wall = False

    if config['algorithms']['path'] == "bfs":
        path = BFS(start, end)


    if print_path:
        convert_ascii(config, grid, "path", path)
        start.icon = "S"
        end.icon = "E"
 
    print_grid_to_file(grid, "solved_maze.txt")

    return grid, path, start, end


if __name__ == "__main__":
    main(print_path=True)
