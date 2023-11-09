from adapters.ibge.ibge_api import IbgeAPI


def get_cities():
    cities_list = IbgeAPI().get_cities()
    return cities_list
