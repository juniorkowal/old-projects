def group_value(coords: tuple, our_map, radius=2):
    """
    Adds additional value to objects next to each other. If the value was < 0 from the beginning then no value is added
    As its a function that checks the surrounding objects value, that value has to be set already
    Adding the value immediately to a function would artificially increase the value of the next object that is next to
    it so the entire map should be, ideally, checked 3 times

    :param hero: Our hero
    :param coords: Coordinates of the tile checked
    :param our_map: Our entire found map
    :param radius: how many squares around the tile are to be checked
    :return: Value to be added to the checked tile
    """
    x, y, = coords[0], coords[1]
    tile = our_map[x, y]
    coords_to_check = []
    numbers = [0]
    value = 0

    # Returns 0 if the value was 0 or less to begin with
    if tile <= 0:
        return 0

    for i in range(1, radius+1):
        numbers.append(i)
        numbers.append(-i)

    for i in numbers:
        for j in numbers:
            if i == 0 and j == 0:
                continue
            x_map = x + i
            y_map = y + j
            if x_map < 0 or y_map < 0:  # So we don't accidentally check items from the back of the list
                continue
            try:
                if type(our_map[x_map, y_map]) == int:
                    continue
                check_tile_value = our_map[x_map, y_map]
                if check_tile_value <= 0:  # Don't add the value of somewhere we don't want to go to
                    continue
                value += check_tile_value

            except IndexError:  # If goes out of the map so it won't break the algorithm
                pass

    return value




