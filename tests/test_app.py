import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data

def test_signup_success():
    response = client.post("/activities/Chess Club/signup?email=tester@mergington.edu")
    assert response.status_code == 200
    assert "Signed up tester@mergington.edu for Chess Club" in response.json()["message"]

    # Clean up: remove the test participant
    client.delete("/activities/Chess Club/unregister?email=tester@mergington.edu")

def test_signup_already_signed_up():
    # Sign up first
    client.post("/activities/Chess Club/signup?email=dupe@mergington.edu")
    # Try again
    response = client.post("/activities/Chess Club/signup?email=dupe@mergington.edu")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]
    # Clean up
    client.delete("/activities/Chess Club/unregister?email=dupe@mergington.edu")

def test_signup_activity_not_found():
    response = client.post("/activities/Nonexistent/signup?email=ghost@mergington.edu")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]

def test_unregister_success():
    # Add, then remove
    client.post("/activities/Chess Club/signup?email=remove@mergington.edu")
    response = client.delete("/activities/Chess Club/unregister?email=remove@mergington.edu")
    assert response.status_code == 200
    assert "Removed remove@mergington.edu from Chess Club" in response.json()["message"]

def test_unregister_not_found():
    response = client.delete("/activities/Chess Club/unregister?email=ghost@mergington.edu")
    assert response.status_code == 404
    assert "Participant not found" in response.json()["detail"]
