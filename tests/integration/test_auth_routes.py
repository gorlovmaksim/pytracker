"""Integration tests for authentication routes."""

def test_login(client, test_user):
    """Test user login functionality."""
    response = client.post('/login',
                         data={'email': 'test@example.com', 'password': 'Test1234!'},
                         follow_redirects=True)
    assert response.status_code == 200