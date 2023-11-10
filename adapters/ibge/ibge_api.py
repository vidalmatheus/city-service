from adapters.ibge import ibge_endpoints


class IbgeAPI:
    def fetch_cities(self):
        resp = ibge_endpoints.GetCities().send()
        cities_list = resp.cleaned
        return cities_list
