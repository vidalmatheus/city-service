import pytest

from adapters.exceptions import IbgeConnectionError
from adapters.ibge.ibge_api import IbgeAPI


def test_fetch_cities(mock_ibge_fetch_cities):
    resp = IbgeAPI().fetch_cities()
    assert resp[0]["name"] == "Abadia de Goiás"
    assert resp[1]["name"] == "Abadia dos Dourados"


def test_ibge_connection_error(mock_ibge_fetch_cities_connection_error):
    error_msg = "IBGE GET https://servicodados.ibge.gov.br/api/v1/localidades/municipios with params={'orderby': 'nome'} json=None data=None connection error"
    with pytest.raises(IbgeConnectionError, match=error_msg):
        IbgeAPI().fetch_cities()
