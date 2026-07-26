from urllib.parse import quote


def test_get_activities_returns_catalog_of_available_activities(client, reset_activities):
    # Arrange
    expected_activity_names = {
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Basketball Team",
        "Swimming Club",
        "Drama Club",
        "Art Workshop",
        "Science Club",
        "Debate Team",
    }

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert set(response.json().keys()) == expected_activity_names


def test_signup_for_activity_adds_new_participant_when_space_is_available(client, reset_activities):
    # Arrange
    activity_name = "Basketball Team"
    email = "newstudent@mergington.edu"

    assert email not in reset_activities[activity_name]["participants"]

    # Act
    response = client.post(
        f"/activities/{quote(activity_name, safe='')}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    assert email in reset_activities[activity_name]["participants"]


def test_signup_for_activity_returns_error_for_duplicate_registration(client, reset_activities):
    # Arrange
    activity_name = "Chess Club"
    email = reset_activities[activity_name]["participants"][0]

    assert email in reset_activities[activity_name]["participants"]

    # Act
    response = client.post(
        f"/activities/{quote(activity_name, safe='')}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_for_activity_returns_error_when_activity_is_missing(client, reset_activities):
    # Arrange
    activity_name = "Unknown Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{quote(activity_name, safe='')}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_participant_removes_email_from_activity(client, reset_activities):
    # Arrange
    activity_name = "Chess Club"
    email = reset_activities[activity_name]["participants"][0]

    assert email in reset_activities[activity_name]["participants"]

    # Act
    response = client.delete(
        f"/activities/{quote(activity_name, safe='')}/participants/{quote(email, safe='')}"
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"
    assert email not in reset_activities[activity_name]["participants"]
