"""Integration tests for habit-related routes."""

def test_add_habit(client, test_user):
    """Test adding a new habit."""

    # Login
    client.post('/login',
                data={'email': 'test@example.com', 'password': 'Test1234!'},
                follow_redirects=True)

    # Add a habit
    response = client.post('/add',
                           data={'name': 'New Habit', 'periodicity': 'daily', 'target_days': '21'},
                           follow_redirects=True)
    assert response.status_code == 200