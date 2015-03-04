from django.core.exceptions import ValidationError
import re


def validate_username(username):
    """
    Checks if the username conforms to the requirements
    :param username:
    :return:
    """
    # minimum length of 3
    if len(username) < 3:
        raise ValidationError("Username is too short, it must be at least 3 letters")
    if len(username) > 20:
        raise ValidationError("Username is too long, it must be less than or equal to 20 letters")
    # whitelist of allowed characters
    if not re.match(r'^[a-zA-Z0-9._]+$', username):
        raise ValidationError("Illegal character(s) in username. Allowed: a-z, A-Z, 0-9, dots(.) and underscores(_)")


def validate_password(password):
    """
    Checks if the password is strong enough
    :param password:
    :return:
    """
    # minimum length
    if len(password) < 8:
        raise ValidationError("Username is too short, it must be at least 3 letters")
    # maximum length
    if len(password) > 25:
        raise ValidationError("Username is too long, it can be at most 25 letters")
    # No further restrictions for now
