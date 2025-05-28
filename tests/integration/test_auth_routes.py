"""
Integration tests for authentication routes.
"""


def test_login(client, test_user):
    """Test user login functionality.

    Args:
        client (FlaskClient): Test client for making requests.
        test_user (User): A fixture providing a test user.
    """
    response = client.post(
        "/login",
        data={"email": "test@example.com", "password": "Test1234!"},
        follow_redirects=True,
    )
    assert response.status_code == 200
