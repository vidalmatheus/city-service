class Method:
    GET = "GET"
    POST = "POST"


class BaseRequest:
    def __init__(self):
        self.cookies = {}
        self.session = self._build_session()

    def _build_session(self):
        raise NotImplementedError("_build_session method not yet implemented")

    def send(self, params: dict = None, json: dict = None, data: dict = None):
        raise NotImplementedError("send method not yet implemented")
