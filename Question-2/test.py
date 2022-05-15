import json
from main import app
import requests


client = app.test_client()


def test_index_route():
    url = '/index'
    response = client.get(url)
    assert response.status_code == 200


def test_create_sport_route():
    url = '/create_sport'
    # response = client.get(url)
    data = {"name": "away-win", "event_id": 2, "price": 2.00, "active": True, "outcome": "void"}
    response = requests.post(url, data)
    result = json.loads(response.text)
    assert response.status_code == 200
    assert result["status"] == 200
