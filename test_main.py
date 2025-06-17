from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_weather_endpoint():
    response = client.get("/weather?city=Colombo&units=metric")
    
    # Check the response status code is OK
    assert response.status_code == 200

    # Check that important keys exist in the returned JSON
    data = response.json()
    assert "temperature" in data
    assert "condition" in data
    assert "humidity" in data
    assert "wind_speed" in data
