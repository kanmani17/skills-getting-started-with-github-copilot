from urllib.parse import quote


def test_unregister_participant_removes_email_from_activity(client, reset_activities):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    assert email in reset_activities[activity_name]["participants"]

    # Act
    response = client.delete(
        f"/activities/{quote(activity_name, safe='')}/participants/{quote(email, safe='')}"
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"

    updated_activities = client.get("/activities").json()
    assert email not in updated_activities[activity_name]["participants"]
