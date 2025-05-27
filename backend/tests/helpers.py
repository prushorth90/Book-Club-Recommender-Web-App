"""Helper methods for unit tests"""

class LogInTester:
    """Tester that checks if a user is logged in."""

    def _is_logged_in(self):
        """Check if the user is logged in."""

        return '_auth_user_id' in self.client.session.keys()
