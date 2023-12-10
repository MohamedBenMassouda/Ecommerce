from django.core.validators import validate_email


def check_user_is_valid(request) -> bool:
    if request.data.get("email") is None or request.data.get("username") is None or request.data.get(
            "password") is None:
        return False

    email = request.data.get("email")

    if not validate_email(email):
        return False

    username = request.data.get("username")
    password = request.data.get("password")

    if len(username) < 4 or len(password) < 4:
        return False

    return True
