import curses, time, yaml
from convert_ascii import convert_ascii
import pathfinder


def animate_path(stdscr, config, term_height, grid, path, start, end):
    stdscr.clear()

    start.icon = "S"
    end.icon = "E"

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

    convert_ascii(config, grid, "path", path)
    offset = 0
    drawn_path = 19
    start.icon = "S"

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
        if i >= len(path) - 1:
            break

    time.sleep(0.1)


def curses_main(stdscr, config):
    curses.curs_set(0)
    curses.start_color()
    start = None
    stdscr.keypad(True)
    stdscr.nodelay(True)

    prev_size = stdscr.getmaxyx()

    while True:
        curr_size = stdscr.getmaxyx()

        if curr_size != prev_size:
            return
        prev_size = curr_size

        term_height, term_width = curr_size[0] - 1, curr_size[1] - 1

        height = 200

        if not start:
            grid, path, start, end = pathfinder.main(config, height, term_width)

        else:
            grid, path, start, end = pathfinder.main(
                config, height, term_width, start=end
            )

        animate_path(stdscr, config, term_height, grid, path, start, end)


def main(config):

    while True:
        curses.wrapper(
            curses_main,
            config,
        )


if __name__ == "__main__":
    with open("config.yaml", "r") as file:
        config = yaml.safe_load(file)

    main(config)
