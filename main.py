""" CSC111 Final Project: Bus Stop Creator
main.py

================================================================================
This is the main file to run the program. This will launch an interactive
pygame screen.
================================================================================
Copyright (c) 2021 Andy Wang, Varun Pillai, Ling Ai, Daniel Liu

city = City.build_from_file("data/map.txt", "data/bus.txt")
city.shortest_path((437,256), (609,273))
"""
# import pygame
from graph_stuff.city_classes import *
from pygame_stuff.drawing import *
from graph_stuff.route_planning import *


def run_visualization(map_file: str = "data/map.txt",
                      bus_file: str = "data/bus.txt",
                      map_save: str = "data/map_save.txt",
                      bus_save: str = "data/bus_save.txt",
                      heuristic: callable = manhattan) -> None:
    """
    Run the interactive city builder. If <input_file> != "", import the city from the file.

    Refer to the project report for a full list of controls.

    Preconditions:
      - input_file and output_file, if specified, are .txt files in the data folder
      - input_file must exist if specified
      - heuristic must be distance, manhattan or diagonal from utility_functions.py
    """
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill(GRASS)  # Initially fill the screen with grass colour

    # Misc variables for running pygame and city
    running = True

    # Used for adding streets; keeps track of endpoints, resets for every two pairs added
    street_pair = []

    city = City()

    # Import a city instead
    if map_file != "" and bus_file != "":
        city = City.build_from_file(map_file, bus_file)

    city.draw(screen)  # Draw at the start

    while running:
        # Get whatever key is pressed
        key = pygame.key.get_pressed()

        # Listen for keys that are HELD DOWN
        running = not key[pygame.K_ESCAPE]
        shift_down = key[pygame.K_LSHIFT]
        ctrl_down = key[pygame.K_LCTRL]
        i_down = key[pygame.K_i]
        s_down = key[pygame.K_s]
        d_down = key[pygame.K_d]

        path = []

        # Check for user mouse input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:  # Check for mouse click
                # Get the user's mouse coordinates
                mouse_pos = pygame.mouse.get_pos()

                if shift_down:  # Shift + click on two places to connect a street
                    place_pos, element_type = city.get_element_from_pos(mouse_pos)

                    if place_pos is None or element_type != "Place":
                        continue
                    elif (place_pos not in street_pair) and (len(street_pair) == 0):
                        # Street_pair is empty, add the first of the pair
                        street_pair.append(place_pos)
                    elif (place_pos not in street_pair) and (len(street_pair) == 1):
                        # Street_pair will have two elements, completing a pair
                        # Add the street and reset street_pair
                        street_pair.append(place_pos)
                        city.add_street(street_pair[0], street_pair[1])
                        street_pair = []

                elif ctrl_down:  # Ctrl + click on a place or a street to remove it
                    element_to_delete, element_type = city.get_element_from_pos(mouse_pos)

                    if element_to_delete is None:
                        continue
                    elif element_type == "Place":
                        city.delete_place(element_to_delete)
                    else:
                        city.delete_street(element_to_delete[0], element_to_delete[1])

                # DIJKSTRA PATHFINDING
                elif s_down:  # s + click to get the shortest path between two places
                    place_pos, element_type = city.get_element_from_pos(mouse_pos)

                    if place_pos is None or element_type == "Street":
                        continue
                    elif (place_pos not in street_pair) and (len(street_pair) == 0):
                        # street_pair is empty, add the first of the pair
                        street_pair.append(place_pos)
                    elif (place_pos not in street_pair) and (len(street_pair) == 1):
                        # street_pair will have two elements, completing a pair
                        # Find the shortest path and reset street_pair
                        street_pair.append(place_pos)
                        path, d = city.dijkstra_path(street_pair[0], street_pair[1])

                        print('Dijkstra pathfinding:')
                        if isinstance(d, str):
                            print(d)
                        else:
                            print(f'\tDistance from {street_pair[0]} '
                                  f'to {street_pair[1]} = {10 * d}m')
                        street_pair = []

                # A* PATHFINDING
                elif d_down:  # d + click to get the 'shortest' path between two places
                    place_pos, element_type = city.get_element_from_pos(mouse_pos)

                    if place_pos is None or element_type == "Street":
                        continue
                    elif (place_pos not in street_pair) and (len(street_pair) == 0):
                        street_pair.append(place_pos)
                    elif (place_pos not in street_pair) and (len(street_pair) == 1):
                        street_pair.append(place_pos)
                        path, d = city.a_star_path(street_pair[0], street_pair[1], heuristic)

                        print('A* pathfinding:')
                        if isinstance(d, str):
                            print(d)
                        else:
                            print(f'\tDistance from {street_pair[0]} '
                                  f'to {street_pair[1]} = {10 * d}m')
                        street_pair = []

                elif city.get_element_from_pos(mouse_pos) == (None, None):
                    # Nothing is being held, so just add a place
                    # But do NOT add a place if the mouse is on top of an already existing place

                    # Hold i to make an intersection
                    if i_down:
                        city.add_place(mouse_pos, kind='intersection')
                    else:
                        city.add_place(mouse_pos)

                # Only need to update the screen when something is added to the city
                screen.fill(GRASS)
                city.draw(screen)
                if len(path) >= 2:
                    color = random.choice(COLOURS)
                    for i in range(len(path)):
                        if i != len(path) - 1:
                            city.draw_highlighted_street((path[i], path[i + 1]), screen,
                                                         color)
                # The advantage of doing this is that the bus stops disappear when you modify
                # the city, and that makes sense

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 and pygame.K_b:
                    # Press 'b1' to override existing bus stops and generate new ones
                    k = city.get_bus_stops_num()

                    # Generate new bus stops by mutating the current city repeatedly
                    # (until we get the best inertia for the k means algorithm),
                    # then display it. Check calculate_inertia() in city_classes.py
                    # on what is inertia. The reason this is done is because a new
                    # inertia exist after projection.
                    counter = 1
                    safety_counter = 1
                    while True:
                        if counter == 5:
                            break
                        temp_inertia = city.add_bus_stops(k)

                        if math.isclose(temp_inertia, city.get_inertia()):
                            counter += 1
                        else:
                            counter = 1
                            city.change_inertia(temp_inertia)
                        safety_counter += 1
                        if safety_counter == 100:
                            break

                    screen.fill(GRASS)
                    city.draw(screen)
                if event.key == pygame.K_2 and pygame.K_b:
                    # get the bus routes!
                    complicated_city = ModelCity(city)
                    complicated_city.generate_city("centered")
                    complicated_city.bus_route_model1()
                    bus_routes = complicated_city.return_bus_routes()
                    for r in bus_routes:
                        city.add_bus_route(r)

                    screen.fill(GRASS)
                    city.draw(screen)
                    for p in bus_routes:
                        if len(p) >= 2:
                            color = random.choice(COLOURS)
                            for i in range(len(p)):
                                if i != len(p) - 1:
                                    city.draw_highlighted_street((p[i], p[i + 1]), screen,
                                                                 color)

                if event.key == pygame.K_s and ctrl_down:  # Ctrl + s to save the city
                    city.export_to_file(map_save, bus_save)

                if event.key == pygame.K_q:  # q to quit
                    running = False

        pygame.display.flip()

    pygame.display.quit()


if __name__ == "__main__":
    run_visualization()
