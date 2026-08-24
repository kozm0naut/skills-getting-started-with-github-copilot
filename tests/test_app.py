from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_signup_and_unregister_participant():
    activity_name = "Chess Club"
    email = "new.student@mergington.edu"

    # arrange
    activity = client.get("/activities").json()[activity_name]
    assert email not in activity["participants"]

    # act: sign up
    signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert signup_response.status_code == 200

    # assert: participant appears
    activity_after_signup = client.get("/activities").json()[activity_name]
    assert email in activity_after_signup["participants"]

    # act: unregister
    unregister_response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
    assert unregister_response.status_code == 200

    # assert: participant removed
    activity_after_unregister = client.get("/activities").json()[activity_name]
    assert email not in activity_after_unregister["participants"]
