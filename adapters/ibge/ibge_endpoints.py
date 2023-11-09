from adapters.base_request import Method
from adapters.ibge.ibge_base import IbgeBaseRequest


class GetCities(IbgeBaseRequest):
    method = Method.GET
    endpoint = "v1/localidades/municipios"

    def send(self, orderby: str = "nome"):
        return super().send(params={"orderby": orderby})

    def clean_response(self, response: list[dict]) -> list[dict]:
        city_list = []
        for city in response:
            city_list.append(
                {"name": city["nome"], "state_abbreviation": city["microrregiao"]["mesorregiao"]["UF"]["sigla"]}
            )
        return city_list
