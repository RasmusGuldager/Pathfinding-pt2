import curses, time
import pathfinder


def animate_path(grid, path, ascii_path, sleep_time, start, end):
    def draw(stdscr):
        curses.curs_set(0)
        curses.start_color()
        stdscr.clear()

        # Draw the static maze
        start.icon = "S"
        end.icon = "E"
        for y, row in enumerate(grid):
            for x, spot in enumerate(row):
                stdscr.addstr(y, x, spot.icon)

        stdscr.refresh()

        pathfinder.convert_ascii(grid, ascii_path, "path", path)
        start.icon = "S"
        end.icon = "E"
        pathfinder.print_grid_to_file(grid, "solved_maze.txt")

        time.sleep(0.5)  # Pause before path animation

        curses.use_default_colors()
        if curses.COLORS >= 256:
            for i, spot in enumerate(path):
                color_code = pathfinder.rainbow_256(i)[1]
                if color_code is not None:
                    pair_number = i + 1  # curses pair numbers must be ≥1
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

        # Animate the path
        for i in range(len(path)):
            for j in range(i + 1):
                spot = path[j]
                y, x = spot.y, spot.x
                icon = spot.icon
                color_attr = getattr(spot, "color_pair", curses.A_NORMAL)
                stdscr.addstr(y, x, icon, color_attr)

            stdscr.refresh()
            time.sleep(sleep_time)

        time.sleep(1)

    curses.wrapper(draw)


def main(update_time, maze_algorithm, path_algorithm, width, height, ascii_maze, ascii_path):
    grid, path, start, end = pathfinder.main(maze_algorithm, path_algorithm, width, height, ascii_maze, ascii_path)

    animate_path(grid, path, ascii_path, update_time, start, end)


if __name__ == "__main__":
    main()
