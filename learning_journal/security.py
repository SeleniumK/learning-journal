import os
from passlib.apps import custom_app_context as pwd_context

USERS = {
    os.environ.get("AUTH_USERNAME"): ['group:users']
}


def groupfinder(userid, request):
    if userid in USERS:
        return USERS.get(userid, [])


def check_username(username):
    auth_users = os.environ.get("AUTH_USERNAME", "not the username")
    if username in auth_users:
        return True


def check_pw(pw):
    hashed = os.environ.get("AUTH_PASSWORD", "not password")
    return pwd_context.verify(pw, hashed)
