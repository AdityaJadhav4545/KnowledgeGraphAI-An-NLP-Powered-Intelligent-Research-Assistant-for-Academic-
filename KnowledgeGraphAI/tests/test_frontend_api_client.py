import requests

from KnowledgeGraphAI.frontend.components.api_client import APIClient


class _Response:
    def __init__(self, status_code, body=None, content=b"", content_type="application/json"):
        self.status_code = status_code
        self.ok = 200 <= status_code < 300
        self.headers = {"content-type": content_type}
        self._body = body
        self.content = content

    def json(self):
        return self._body


class _Session:
    def __init__(self, response=None, exception=None):
        self.response = response
        self.exception = exception
        self.kwargs = None

    def request(self, *_args, **kwargs):
        self.kwargs = kwargs
        if self.exception:
            raise self.exception
        return self.response


def test_client_centralizes_url_auth_timeout_and_json_errors():
    session = _Session(_Response(503, {"detail": {"stage": "graph", "message": "offline"}}))
    client = APIClient("http://backend.test/", "local-key", session)

    result = client.post("/api/papers/1/process", timeout=60, json_body={"force": True})

    assert result.status_code == 503
    assert result.error == "graph: offline"
    assert session.kwargs["headers"] == {"X-API-Key": "local-key"}
    assert session.kwargs["timeout"] == 60
    assert session.kwargs["json"] == {"force": True}


def test_client_returns_binary_source_response_without_json_decoding():
    session = _Session(
        _Response(200, content=b"%PDF-1.7", content_type="application/pdf")
    )
    result = APIClient("http://backend.test", session=session).get(
        "/api/papers/3/source"
    )

    assert result.ok
    assert result.data == b"%PDF-1.7"
    assert result.content_type == "application/pdf"


def test_client_surfaces_unreachable_backend_instead_of_empty_success():
    session = _Session(exception=requests.ConnectionError("refused"))
    result = APIClient("http://backend.test", session=session).get("/api/papers")

    assert not result.ok
    assert not result.available
    assert "Could not reach the backend" in result.error
