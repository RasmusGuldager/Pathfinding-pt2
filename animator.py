import curses, time
import pathfinder


def animate_path(stdscr, grid, path, ascii_path, sleep_time, start, end):
    stdscr.clear()

    start.icon = "S"
    end.icon = "E"
    for y, row in enumerate(grid):
        for x, spot in enumerate(row):
            stdscr.addstr(y, x, spot.icon)
        stdscr.refresh()
        time.sleep(0)


    pathfinder.convert_ascii(grid, ascii_path, "path", path)
    start.icon = "S"
    end.icon = "E"
    pathfinder.print_grid_to_file(grid, "solved_maze.txt")

    time.sleep(0.5)

    curses.use_default_colors()
    if curses.COLORS >= 256:
        for i, spot in enumerate(path):
            color_code = pathfinder.rainbow_256(i)[1]
            if color_code is not None:
                pair_number = i + 1
                try:
                    curses.init_pair(pair_number, color_code, -1)
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
            stdscr.addstr(y, x, icon, color_attr)

        stdscr.refresh()
        time.sleep(sleep_time)

    time.sleep(0.1)


def curses_main(stdscr, update_time, maze_algorithm, path_algorithm, term_width, term_height, ascii_maze, ascii_path):
    curses.curs_set(0)
    curses.start_color()
    start = None

    while True:
        term_height, term_width = stdscr.getmaxyx()
        term_height -= 1
        if not start:
            grid, path, start, end = pathfinder.main(
            maze_algorithm, path_algorithm, term_width, term_height, ascii_maze, ascii_path
        )
        else:
            grid, path, start, end = pathfinder.main(
            maze_algorithm, path_algorithm, term_width, term_height, ascii_maze, ascii_path, start=end
        )

        animate_path(stdscr, grid, path, ascii_path, update_time, start, end)


def main(update_time, maze_algorithm, path_algorithm, term_width, term_height,
         ascii_maze, ascii_path):
    
    curses.wrapper(
        curses_main,
        update_time, 
        maze_algorithm, 
        path_algorithm, 
        term_width, 
        term_height, 
        ascii_maze, 
        ascii_path
    )

if __name__ == "__main__":
    main()
