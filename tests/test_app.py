from urllib.parse import quote

import pytest

ACTIVITY_NAME = "Chess Club"
EXISTING_EMAIL = "michael@mergington.edu"
NEW_EMAIL = "newstudent@mergington.edu"
INVALID_ACTIVITY = "Nonexistent Club"


def test_get_activities(client):
    response = client.get("/activities")
    assert response.status_code == 200
    payload = response.json()
    assert "Chess Club" in payload
    assert "Programming Class" in payload
    assert isinstance(payload[ACTIVITY_NAME]["participants"], list)


def test_signup_for_activity_success(client):
    response = client.post(
        f"/activities/{quote(ACTIVITY_NAME)}/signup",
        params={"email": NEW_EMAIL}
    )
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {NEW_EMAIL} for {ACTIVITY_NAME}"}


def test_signup_for_activity_already_signed_up(client):
    response = client.post(
        f"/activities/{quote(ACTIVITY_NAME)}/signup",
        params={"email": EXISTING_EMAIL}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_for_activity_not_found(client):
    response = client.post(
        f"/activities/{quote(INVALID_ACTIVITY)}/signup",
        params={"email": NEW_EMAIL}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_participant_success(client):
    response = client.delete(
        f"/activities/{quote(ACTIVITY_NAME)}/participants",
        params={"email": EXISTING_EMAIL}
    )
    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {EXISTING_EMAIL} from {ACTIVITY_NAME}"}


def test_unregister_participant_not_found(client):
    response = client.delete(
        f"/activities/{quote(ACTIVITY_NAME)}/participants",
        params={"email": NEW_EMAIL}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in activity"
