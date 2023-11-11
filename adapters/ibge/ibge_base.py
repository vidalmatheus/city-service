import requests
import urllib3
from requests.adapters import HTTPAdapter, Retry
from urllib3.util.ssl_ import create_urllib3_context

from adapters.base_request import BaseRequest
from adapters.exceptions import IbgeConnectionError
from adapters.response_wrapper import ResponseWrapper

BASE_URL = "https://servicodados.ibge.gov.br/api"


class CustomSslContextHttpAdapter(HTTPAdapter):
    """
    Transport adapter" that allows us to use a custom ssl context object with the requests.
    """

    def init_poolmanager(self, connections, maxsize, block=False):
        ctx = create_urllib3_context()
        ctx.load_default_certs()
        ctx.options |= 0x4  # ssl.OP_LEGACY_SERVER_CONNECT
        self.poolmanager = urllib3.PoolManager(ssl_context=ctx)


class IbgeBaseRequest(BaseRequest):
    def _build_session(self):
        session = requests.Session()
        retry_params = dict(total=3, backoff_factor=1, raise_on_status=False)
        retry_strategy = Retry(**retry_params)
        ctx = create_urllib3_context()
        ctx.load_default_certs()
        ctx.options |= 0x4  # ssl.OP_LEGACY_SERVER_CONNECT
        adapter = CustomSslContextHttpAdapter(max_retries=retry_strategy)
        session.mount("https://", adapter)
        return session

    def send(self, params: dict = None, json: dict = None, data: dict = None) -> ResponseWrapper:
        url = f"{BASE_URL}/{self.endpoint}"
        try:
            response = self.session.request(
                method=self.method,
                url=url,
                params=params,
                json=json,
                cookies=self.cookies,
                timeout=10,
                data=data,
                verify=True,
            )
        except ConnectionError as exc:
            error_msg = f"IBGE {self.method} {url} with {params=} {json=} {data=} connection error"
            raise IbgeConnectionError(error_msg) from exc

        response.raise_for_status()

        return ResponseWrapper(self, response)
