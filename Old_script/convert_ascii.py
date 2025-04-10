def convert_ascii(config, grid, condition, path=None):
    if condition == "wall":
        ascii_representation = config["ascii"]["maze"]
        ascii_representation = config["ascii_sets"][ascii_representation]

        for row in grid:
            for spot in row:
                if spot.wall:
                    wall_count = 0
                    directions = []
                    for neighbor in spot.path_neighbors:
                        if neighbor.wall:
                            wall_count += 1
                            directions.append(
                                direction(neighbor.x - spot.x, neighbor.y - spot.y)
                            )
                    update_spot_icon(spot, directions, wall_count, ascii_representation)

    elif condition == "path":
        ascii_representation = config["ascii"]["path"]
        ascii_representation = config["ascii_sets"][ascii_representation]

        for spot in path:
            wall_count = 0
            directions = []
            for neighbor in spot.path_neighbors:
                if neighbor in path:
                    wall_count += 1
                    directions.append(
                        direction(neighbor.x - spot.x, neighbor.y - spot.y)
                    )
            update_spot_icon(spot, directions, wall_count, ascii_representation)

    return grid


def update_spot_icon(spot, directions, wall_count, ascii_representation):
    if wall_count == 1:
        if "E" in directions or "W" in directions:
            spot.icon = ascii_representation[0]
        else:
            spot.icon = ascii_representation[1]
    elif wall_count == 2:
        if "E" in directions and "W" in directions:
            spot.icon = ascii_representation[0]
        elif "N" in directions and "S" in directions:
            spot.icon = ascii_representation[1]
        elif "S" in directions and "E" in directions:
            spot.icon = ascii_representation[2]
        elif "S" in directions and "W" in directions:
            spot.icon = ascii_representation[3]
        elif "N" in directions and "E" in directions:
            spot.icon = ascii_representation[4]
        elif "N" in directions and "W" in directions:
            spot.icon = ascii_representation[5]
    elif wall_count == 3:
        if "N" in directions and "S" in directions and "E" in directions:
            spot.icon = ascii_representation[6]
        elif "N" in directions and "S" in directions and "W" in directions:
            spot.icon = ascii_representation[7]
        elif "E" in directions and "W" in directions and "S" in directions:
            spot.icon = ascii_representation[8]
        elif "E" in directions and "W" in directions and "N" in directions:
            spot.icon = ascii_representation[9]
    elif wall_count == 4:
        spot.icon = ascii_representation[10]
    else:
        print("Error: Invalid wall count")


def direction(x, y):
    if x == 0 and y == -1:
        return "S"
    if x == 1 and y == 0:
        return "E"
    if x == 0 and y == 1:
        return "N"
    if x == -1 and y == 0:
        return "W"
