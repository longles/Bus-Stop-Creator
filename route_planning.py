"""
route planning

Assume that we auto generating a bus route system that only uses 1 type of bus, like
the mini bus network in hong kong.
"""
import random

from graph_stuff.city_classes import *
from graph_stuff.city_classes import _Place
from graph_stuff.city_classes import _BusStop
from utility_functions import *


class ComplicatedPlace(_Place):
    """
    A more complicated place class with one more parameter: the population density

    Instance Attributes:
        - population_density: population density of the place (people amount per km squared)
    """
    pos: tuple[float, float]
    neighbours: dict[_Place, float]
    population_density: int  # per km squared

    def __init__(self, place: _Place) -> None:
        super().__init__(copy.deepcopy(place.pos))
        self.neighbours = copy.deepcopy(place.neighbours)
        self.population_density = 0

    def set_density(self, density: int) -> None:
        """
        set the population density
        """
        self.population_density = density


class PlacePair:
    """
    Represents 2 vertex in the City graph that is not a bus stop

    Instance Attributes:
        - coords: the coordinates of the two bus stops
    """
    coords: tuple[tuple[float, float], tuple[float, float]]
    path1flow: int  # passengers that need to travel from coords[0] to coords[1] in 1 hour (avg)
    path2flow: int  # passengers that need to travel from coords[1] to coords[0] in 1 hour (avg)

    # frequency: int  # number of times vehicles are employed over 1 hour

    def __init__(self, coords: tuple[tuple[float, float], tuple[float, float]]) -> None:
        self.coords = coords
        self.path1flow = 0
        self.path2flow = 0

    def set_flow(self, pathflow1: int, pathflow2: int) -> None:
        """
        set the path1flow, path2flow of this edge
        """
        self.path1flow = pathflow1
        self.path2flow = pathflow2


def avg_flow(pair: PlacePair) -> int:
    """
    return the average flow of a PlacePair
    """
    return int((pair.path1flow + pair.path2flow) / 2)


class ModelCity(City):
    """
    A slightly modified city class for route generation modeling
    """
    _places: dict[tuple, ComplicatedPlace]
    _streets: set[tuple[tuple, tuple]]
    _bus_stops: dict[tuple: _BusStop]
    _bus_routes: list[list[tuple]]
    _place_pairs: list[PlacePair]
    _simple_city: City

    def __init__(self, city: City) -> None:
        super().__init__()
        self._places = {index: ComplicatedPlace(city._places[index]) for index in city._places}
        self._streets = copy.deepcopy(city._streets)
        self._bus_stops = copy.deepcopy(city._bus_stops[0])
        self._bus_routes = copy.deepcopy(city._bus_routes)
        self._place_pairs = []
        self._simple_city = city

    def return_bus_routes(self) -> list:
        """
        return the bus routes
        """
        return self._bus_routes

    def generate_city(self, city_type: str) -> None:
        """
        generate a city of city_type for testing

        city_type == "centered":
        made sure several places in this city has a high population density (city centers)

        city_type == "distributed":
        randomly assign places with population densities

        There are two ideologies for the auto generation mode centered:
        1. take a pair of places A and B, the flow from A to B and B to A should be similar
        in a city (people who go work/play in another place will return)
        2. flow to densed areas should be larger


        precondition
            - len(self._places) > 1
        """
        places = [self._places[index] for index in self._places]
        if city_type == "centered":
            center_num = len(self._places) // 10
            if center_num == 0:
                center_num = 1
            center_coords = []
            for _ in range(center_num):
                city_center = random.choice([self._places[index] for index in self._places])
                city_center.population_density = random.randint(6000, 7000)
                center_coords.append(city_center.pos)

            for place in places:
                if place.pos not in center_coords:
                    place.population_density = random.randint(1000, 2000)

        elif city_type == "distributed":
            start_density = random.randint(100, 10000)
            for place in places:
                place.population_density = start_density * random.uniform(0.8, 1.2)

        place_pairs = []
        for place1 in places:
            for place2 in places:
                if (place2.pos, place1.pos) not in place_pairs\
                        and place1.pos != place2.pos:
                    place_pairs.append((place1.pos, place2.pos))
                    place_pair = PlacePair((place1.pos, place2.pos))

                    if place1.population_density < place2.population_density:
                        # proportion = place1.population_density / place2.population_density
                        place_pair.set_flow(int(place2.population_density
                                                * random.uniform(0.5, 0.55)),
                                            int(place2.population_density
                                                * random.uniform(0.5, 0.55)))
                    else:
                        # proportion = place2.population_density / place1.population_density
                        place_pair.set_flow(int(place1.population_density
                                                * random.uniform(0.5, 0.55)),
                                            int(place1.population_density
                                                * random.uniform(0.5, 0.55)))
                    self._place_pairs.append(place_pair)

    def bus_route_model1(self) -> None:
        """
        model 1 of trying to generate bus routes

        The strategy is to design bus routes where the edges with the most flow are covered;
        also make sure

        city = City.build_from_file("data/map_save.txt", "data/bus_save.txt")
        City = ModelCity(city)
        City.generate_city("centered")
        City.bus_route_model1()

        City.merge_route([(691, 477), (609, 273), (544, 250), (437, 256),
        (381, 195), (246, 226)], [(381, 195), (246, 226)])
        """
        if self._bus_stops == dict():
            return
        self._bus_routes = []
        self._place_pairs.sort(key=avg_flow, reverse=True)
        bus_stops = list(self._bus_stops)
        potential_paths = []
        for pair in self._place_pairs:
            distance1 = []
            for coord in bus_stops:
                distance1.append(distance(coord, pair.coords[0]))
            b1 = bus_stops[distance1.index(min(distance1))]

            distance2 = []
            for coord in bus_stops:
                distance2.append(distance(coord, pair.coords[1]))
            b2 = bus_stops[distance2.index(min(distance2))]

            path = self._simple_city.dijkstra_path(b1, b2)
            potential_paths.append(path[0])

        routes = []
        for p in potential_paths:
            for coordinate in p:
                if coordinate in bus_stops:
                    bus_stops.remove(coordinate)
            if p != []:
                routes.append(p)
            if bus_stops == []:
                break

        routes2 = copy.copy(routes)
        # print(routes2)
        for r in routes:
            for r2 in routes:
                if r != r2 and r in routes2 and r2 in routes2:
                    merged_route = self.merge_route(r, r2)
                    if merged_route != []:
                        self._bus_routes.append(merged_route)
                        routes2.remove(r)
                        routes2.remove(r2)
        # print(routes2)
        for r in routes2:
            self._bus_routes.append(r)

    def merge_route(self, lst1: list, lst2: list) -> list:
        """
        [(691, 477), (609, 273), (544, 250), (437, 256), (381, 195), (246, 226)]
        [(540, 500), (457, 417), (437, 256), (381, 195), (246, 226)]
        [(381, 195), (246, 226)]
        """
        lst1_overlap = []
        for element in lst1:
            lst1_overlap.append(element in lst2)

        lst2_overlap = []
        for element in lst2:
            lst2_overlap.append(element in lst1)

        consecutive_counter = 0
        for i in range(len(lst1_overlap)):
            if lst1_overlap[i] and consecutive_counter == 0:
                consecutive_counter += 1
            elif lst1_overlap[i] and lst1_overlap[i - 1]:
                consecutive_counter += 1
            else:
                consecutive_counter = 0

        consecutive_counter2 = 0
        for i in range(len(lst2_overlap)):
            if lst2_overlap[i] and consecutive_counter2 == 0:
                consecutive_counter2 += 1
            elif lst2_overlap[i] and lst2_overlap[i - 1]:
                consecutive_counter2 += 1
            else:
                consecutive_counter2 = 0

        # print(lst1_overlap, lst2_overlap)
        # if the repeated elements are not consecutive, cannot merge
        if consecutive_counter2 != sum(lst2_overlap) or \
                consecutive_counter != sum(lst1_overlap):
            return []
        # so now we are sure the repeated elements are consecutive
        # are the repeated elements on the edge of the list for both list though?
        elif not((lst1_overlap[0] or lst1_overlap[-1])
                 and (lst2_overlap[0] or lst2_overlap[-1])):
            # the repeated elements are not on the edge of the list for both list
            # then test for if a list is completely part of the other list
            if lst1_overlap[0] and lst1_overlap[-1]:
                return lst2
            elif lst2_overlap[0] or lst2_overlap[-1]:
                return lst1
            # if not, return []
            else:
                return []
        # so the repeated elements are on the edge of the list for both lists
        else:
            if (lst1[0] == lst2[0] and lst1[1] == lst2[1]) or (
                    lst1[-2] == lst2[-2] and lst1[-1] == lst2[-1]):
                if len(lst1) != 2 and len(lst2) != 2:
                    return []
                elif len(lst1) == 2:
                    return lst2
                else:
                    return lst1
            elif lst1[0] == lst2[-1] and lst1[1] == lst2[-2]:
                for _ in range(sum(lst1_overlap)):
                    lst1.pop(0)
                return lst2 + lst1
            elif lst1[-1] == lst2[0] and lst1[-2] == lst2[1]:
                for _ in range(sum(lst2_overlap)):
                    lst2.pop(0)
                return lst1 + lst2
            else:
                return []

    def analyse_street(self) -> None:
        """
        .
        """


if __name__ == '__main__':
    import python_ta.contracts
    python_ta.contracts.check_all_contracts()

    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['graph_stuff.city_classes', 'utility_functions', 'copy', 'random'],
        'allowed-io': [],
        'max-line-length': 100,
        'disable': ['E1136']
    })
