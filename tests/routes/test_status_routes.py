import json


def test_status(client):
    resp = client.get("/status")
    assert resp.status_code == 200
    json_resp = json.loads(resp.content)
    assert json_resp["status"] == "ok"
