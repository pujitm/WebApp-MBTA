import json
import requests
from dotenv import load_dotenv
from os import environ
from scipy import spatial


def create_url_builder(base_url):
    """Quick, shitty tool to build api endpoints.

    Pass in base api url to get a new function. Pass it an endpoint and get the fully formed url path.

    Args:
        base_url (string): domain of api. Prefer to omit trailing slash.

    Returns:
        func(api_route (string)) -> string : Returns full url of api endpoint
    """
    return lambda route: base_url + route


load_dotenv()
MAPQUEST_API_KEY = environ.get("MAPQUEST_API_KEY")
MAPQUEST_BASE_URL = environ.get("MAPQUEST_BASE_URL")


def prepare_mbta_stop_data(stops):
    """Read MBTA station data (megabytes) and parse into read-only data collections for querying and access

    Args:
        stops (list[station_data]): Pre-processed MBTA station data. List of JSON objects.

    Returns:
        dictionary: {
            stops(list[station_data]): Pre-processed MBTA station data. List of JSON objects. Reference to parameter,
            stop_coordinates_tree (scipy.spatial.KDTree): (float, float) lat,long coordinate tuples linked to each entry in `stops`
        }
    """
    get_coordinates = lambda stop: (stop["lat"], stop["long"])
    stop_coordinates = [get_coordinates(stop) for stop in stops]
    return {
        "stops": stops,
        "stop_coordinates_tree": spatial.KDTree(stop_coordinates),
    }


def get_lat_long(place_name):
    """Given a string representing a place, return (latitude, longitude) tuple

    Args:
        place_name (string): Arbitrary place (e.g. Washington D.C.)

    Returns:
        (float, float): Latitude, Longitude coordinate pair
    """
    url_params = {"key": MAPQUEST_API_KEY, "location": place_name}
    endpoint = create_url_builder(MAPQUEST_BASE_URL)("/address")
    response = requests.get(endpoint, params=url_params).json()
    coordinates = response["results"][0]["locations"][0]["latLng"]
    return (coordinates["lat"], coordinates["lng"])


def get_nearest_station(coordinates, stops_collections):
    """Given latitude,longitude coordinates, find nearest station in `stop_collections`

    Args:
        coordinates (float, float): Latitude, Longitude
        stops_collections (IStop_Collections): see `prepare_mbta_stop_data` for interface shape

    Returns:
        dictionary/object: info representing an MBTA station
    """
    coordinate_tree = stops_collections["stop_coordinates_tree"]
    # https://stackoverflow.com/a/39109296/6656631 -- using k-dim trees to find closest coordinate pair in set
    results = coordinate_tree.query([coordinates])
    # K-Dimensional Tree Query Parsing -- https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.KDTree.query.html#scipy.spatial.KDTree.query
    stop_index = list(results[1])[0]
    return stops_collections["stops"][stop_index]


def find_stop_near(place_name, stop_collections):
    """
    Given a place name or address, return the nearest MBTA stop and whether it is wheelchair accessible.
    """
    return get_nearest_station(
        get_lat_long(place_name), stops_collections=stop_collections
    )


def get_stop_collections():
    from_filename = "filtered_mbta_stop_data.json"
    with open(from_filename) as stop_data_file:
        stops = json.load(stop_data_file)
        return prepare_mbta_stop_data(stops=stops)


def main():
    """
    You can test all the functions here
    """
    collections = get_stop_collections()
    print(find_stop_near("Babson College", stop_collections=collections))
    print(find_stop_near("Boston", stop_collections=collections))


if __name__ == "__main__":
    main()
