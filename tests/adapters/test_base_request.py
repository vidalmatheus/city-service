import pytest

from adapters.base_request import BaseRequest


def test_not_implemented__build_session():
    class MyBaseRequest(BaseRequest):
        pass

    with pytest.raises(NotImplementedError, match="_build_session method not yet implemented"):
        MyBaseRequest()


def test_not_implemented_send():
    class MyBaseRequest(BaseRequest):
        def _build_session(self):
            return None

    with pytest.raises(NotImplementedError, match="send method not yet implemented"):
        MyBaseRequest().send()
