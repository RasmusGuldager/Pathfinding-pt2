import curses, time, yaml, random
from convert_ascii import convert_ascii
import pathfinder


def animate_path(stdscr, config, grid, path, start, end):
    stdscr.clear()

    start.icon = "S"
    end.icon = "E"
    for y, row in enumerate(grid):
        for x, spot in enumerate(row):
            try:
                stdscr.addstr(y, x, spot.icon)
            except curses.error:
                pass
        stdscr.refresh()
        # time.sleep(0.1)

    ascii_path = config["ascii"]["path"]
    ascii_path = config["ascii_sets"][ascii_path]

    convert_ascii(config, grid, "path", path)
    start.icon = "S"
    end.icon = "E"

    # time.sleep(0.5)

    curses.use_default_colors()
    if curses.COLORS >= 256:
        for i, spot in enumerate(path):
            if spot.color_code is not None:
                pair_number = i + 1
                try:
                    curses.init_pair(pair_number, spot.color_code, -1)
                    spot.color_pair = curses.color_pair(pair_number)
                except curses.error:
                    spot.color_pair = curses.A_NORMAL
            else:
                spot.color_pair = curses.A_NORMAL
    else:
        for spot in path:
            spot.color_pair = curses.A_NORMAL

    for i in range(len(path)):
        for j in range(i + 1):
            spot = path[j]
            y, x = spot.y, spot.x
            icon = spot.icon
            color_attr = getattr(spot, "color_pair", curses.A_NORMAL)
            try:
                stdscr.addstr(y, x, icon, color_attr)
            except curses.error:
                pass

        stdscr.refresh()
        time.sleep(config["update_time"])

    # time.sleep(0.5)


def curses_main(stdscr, config):
    curses.curs_set(0)
    curses.start_color()
    start = None
    stdscr.keypad(True)
    stdscr.nodelay(True)

    prev_size = stdscr.getmaxyx()

    while True:
        curr_size = stdscr.getmaxyx()
        key = stdscr.getch()

        if curr_size != prev_size:
            return

        term_height, term_width = curr_size[0] - 1, curr_size[1] - 1

        if not start:
            grid, path, start, end = pathfinder.main(config, term_height, term_width)

        else:
            grid, path, start, end = pathfinder.main(
                config, term_height, term_width, start=end
            )

        animate_path(stdscr, config, grid, path, start, end)


def main(config):

    while True:
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
        if random.randint(0, 15) == 0:
            print("\n🗝️  You found a secret exit from the maze.\n")
        else:
            print("Closed maze\n")
