import curses, time, yaml, random
from convert_ascii import convert_ascii, rainbow_256
import pathfinder


def animate_path(
    stdscr, config, term_height, term_width, grid, path, height, end, random_seed
):
    stdscr.clear()

    for y, row in enumerate(grid):
        if y >= term_height:
            break
        for x, spot in enumerate(row):
            try:
                stdscr.addstr(y, x, spot.icon)
            except curses.error:
                pass
        stdscr.refresh()
        time.sleep(0.01)

    ascii_path = config["ascii"]["path"]
    ascii_path = config["ascii_sets"][ascii_path]

    time.sleep(0.5)

    convert_ascii(config, grid, "path", path)
    offset = 0
    drawn_path = 19

    for i in range(19):
        for j in range(offset, i + 1):
            spot = path[j]
            y, x = spot.y, spot.x
            color_attr = getattr(spot, "color_pair", curses.A_NORMAL)
            try:
                stdscr.addstr(y, x, spot.icon, color_attr)
            except curses.error:
                pass

        stdscr.refresh()
        time.sleep(config["update_time"])

    while True:
        # Draw maze with already drawn path
        for y, row in enumerate(grid):
            if y >= term_height + offset:
                break
            elif y < offset:
                continue
            for x, spot in enumerate(row):
                try:
                    if spot.wall:
                        stdscr.addstr(y - offset, x, spot.icon)
                    elif spot.path_id < drawn_path:
                        color_attr = getattr(spot, "color_pair", curses.A_NORMAL)
                        stdscr.addstr(y - offset, x, spot.icon, color_attr)
                    else:
                        stdscr.addstr(y - offset, x, " ")
                except curses.error:
                    pass
        stdscr.refresh()

        # Clear bottom of screen if maze is smaller than terminal size
        if y < term_height + offset:
            while y - offset < term_height:
                for x in range(len(row)):
                    try:
                        stdscr.addstr(y - offset + 1, x, " ")
                    except curses.error:
                        pass
                y += 1

        # Draw path
        for i in range(len(path)):
            if path[i].y >= offset + 20:
                offset += 1
                drawn_path = path[i].path_id
                break
            elif path[i].path_id < drawn_path:
                continue

            for j in range(offset, i + 1):
                spot = path[j]
                y, x = spot.y - offset, spot.x
                color_attr = getattr(spot, "color_pair", curses.A_NORMAL)
                try:
                    stdscr.addstr(y, x, spot.icon, color_attr)
                except curses.error:
                    pass

            stdscr.refresh()
            time.sleep(config["update_time"])

        if offset % height - 1 == 0:
            end = generate_new_grid(
                config, term_width, height, grid, path, end, random_seed
            )
            convert_ascii(config, grid, "path", path)

        if i >= len(path) - 1:
            break

    time.sleep(0.5)


def curses_main(stdscr, config):
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()
    stdscr.keypad(True)
    stdscr.nodelay(True)

    curr_size = stdscr.getmaxyx()

    height = 20
    term_height, term_width = curr_size[0] - 1, curr_size[1] - 1

    height += height % 2 == 0

    grid, path, end = setup(config, term_width, height)

    iterations = 3
    random_seed = random.randint(0, 255)

    for i in range(iterations):
        end = generate_new_grid(
            config, term_width, height, grid, path, end, random_seed
        )

    animate_path(
        stdscr, config, term_height, term_width, grid, path, height, end, random_seed
    )


def setup(config, term_width, height):
    grid, path, end = pathfinder.main(config, height, term_width)
    grid.pop()
    path.pop()

    for spot in range(len(path)):
        path[spot].path_id = spot

    for row in grid:
        for spot in row:
            spot.find_path_neighbors(grid)

    return grid, path, end


def generate_new_grid(config, term_width, height, grid, path, end, random_seed):
    temp_grid, temp_path, end = pathfinder.main(config, height, term_width, start=end)
    temp_grid.pop()
    temp_path.pop()

    for spot in temp_path:
        spot.path_id = path[-1].path_id + 1
        path.append(spot)

    for row in temp_grid:
        for spot in row:
            spot.y = grid[-1][-1].y + spot.y + 1

    grid.extend(temp_grid)

    for row in grid:
        for spot in row:
            spot.find_path_neighbors(grid)

    for i in range(len(path)):
        path[i].color_code = rainbow_256(i + random_seed, config["frequency"])

    # Set color pairs for path
    if curses.COLORS >= 256:
        for i, spot in enumerate(path):
            if spot.color_code is not None:
                pair_number = i + 1
                curses.init_pair(pair_number, spot.color_code, -1)
                spot.color_pair = curses.color_pair(pair_number)

    convert_ascii(config, grid, "wall")

    return end


def main(config):
    curses.wrapper(
        curses_main,
        config,
    )


if __name__ == "__main__":
    try:
        with open("config.yaml", "r") as file:
            config = yaml.safe_load(file)

        main(config)

    except KeyboardInterrupt:
        if random.randint(0, 10) == 0:
            print("\n 🗝️  You found a secret exit from the maze 🗝️\n")
        else:
            print("Closed maze\n")
