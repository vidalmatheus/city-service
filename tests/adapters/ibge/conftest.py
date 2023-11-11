import pytest
from requests_mock.mocker import Mocker

from adapters.ibge.ibge_base import BASE_URL
from adapters.ibge.ibge_endpoints import GetCities
from tests.adapters.ibge.mock_responses import mock_ibge_get_cities


@pytest.fixture
def mock_ibge_fetch_cities(requests_mock: Mocker):
    return requests_mock.get(
        url=f"{BASE_URL}/{GetCities.endpoint}",
        json=mock_ibge_get_cities.response,
        status_code=200,
    )


@pytest.fixture
def mock_ibge_fetch_cities_connection_error(requests_mock: Mocker):
    return requests_mock.get(url=f"{BASE_URL}/{GetCities.endpoint}", exc=ConnectionError)
