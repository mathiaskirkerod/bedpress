# Fixed password from env
import os

FIXED_PASSWORD = os.environ.get("REACT_APP_API_PASSWORD", "AbakusErEnKalkulator")


def authenticate_user(name: str, password: str) -> str:
    """
    Authenticate a user with the fixed password

    Args:
        name: User's name
        password: Password to validate

    Returns:
        The authenticated username if successful
        None if authentication fails
    """
    if password == FIXED_PASSWORD:
        return name

    # Return None instead of raising an exception
    return None
