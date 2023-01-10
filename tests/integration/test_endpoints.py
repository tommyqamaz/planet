from http import HTTPStatus

from fastapi.testclient import TestClient


def test_classes(client: TestClient):

    response = client.get("/planet/classes")
    assert response.status_code == HTTPStatus.OK

    genres = response.json()["classes"]

    assert isinstance(genres, list)


def test_predict(client: TestClient, sample_image_bytes: bytes):

    files = {
        "image": sample_image_bytes,
    }
    response = client.post("/planet/predict", files=files)

    assert response.status_code == HTTPStatus.OK

    predicted_weather = response.json()["result"]

    assert isinstance(predicted_weather, list)


def test_predict_proba(client: TestClient, sample_image_bytes: bytes):

    files = {
        "image": sample_image_bytes,
    }
    response = client.post("/planet/predict_proba", files=files)

    assert response.status_code == HTTPStatus.OK

    weather2prob = response.json()

    for weather_prob in weather2prob["result"]:
        assert weather_prob < 1
        assert weather_prob > 0
