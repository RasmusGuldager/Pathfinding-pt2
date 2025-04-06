def print_grid_to_file(grid, file):
    with open(f"text_files/{file}", "w") as f:
        for row in grid:
            for spot in row:
                if getattr(spot, "color", None):
                    f.write(f"{spot.color}{spot.icon}\033[0m")
                else:
                    f.write(spot.icon)
            f.write("\n")
