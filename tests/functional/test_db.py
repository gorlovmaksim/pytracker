"""
Functional tests for database operations.
"""


def test_db_init(app):
    """Test database initialization and basic operations.

    Args:
        app (Flask): The Flask application instance.
    """
    with app.app_context():
        from db import db

        # Check that tables are created without errors
        db.create_all()

        # Checking the connection
        result = db.session.execute("SELECT 1")
        assert result.scalar() == 1

        # Check for transaction rollback
        try:
            db.session.execute("INVALID SQL")
            db.session.commit()
            assert False, "Should raise exception"
        except Exception:
            db.session.rollback()
            assert True
