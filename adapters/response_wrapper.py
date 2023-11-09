class ResponseWrapper:
    def __init__(self, request, response):
        self.request = request
        self.response = response

    @property
    def raw(self):
        return self.response.json()

    @property
    def cleaned(self):
        return self.request.clean_response(self.raw)
