import os
AUTH_DATA = {"username": "seleniumk", "password": "python"}


def test_access_to_view(authenticated_app):
    response = authenticated_app.get('/write')
    assert response.status_code == 200


# def test_redirect_unvalidated_user(app):
#     response = app.get('/write', status='403')
#     assert response.status_code == 403
#     headers = response.headers
#     domain = "http://localhost"
#     actual_path = headers.get('Location', '')[len(domain):]
#     assert actual_path == "/login"


def test_username_exists(auth_env):
    assert os.environ.get('AUTH_USERNAME', None) is not None


def test_password_exists(auth_env):
    assert os.environ.get('AUTH_PASSWORD', None) is not None


def test_pass_encrypted(auth_env):
    assert os.environ.get("AUTH_USERNAME", None) != "python"


def test_check_pw_success(auth_env):
    from learning_journal.security import check_pw
    password = 'python'
    assert check_pw(password)


def test_check_pw_fails(auth_env):
    from learning_journal.security import check_pw
    password = 'not python'
    assert not check_pw(password)


def test_check_username_success(auth_env):
    from learning_journal.security import check_username
    username = 'seleniumk'
    assert check_username(username)


def test_check_username_fails(auth_env):
    from learning_journal.security import check_username
    username = 'someone else'
    assert not check_username(username)


def test_get_login_view(app):
    response = app.get('/login')
    assert response.status_code == 200


def test_post_login_success(app, auth_env):
    response = app.post('/login', AUTH_DATA)
    assert response.status_code == 302


def test_post_login_success_redirects_home(app, auth_env):
    response = app.post('/login', AUTH_DATA)
    headers = response.headers
    domain = "http://localhost"
    actual_path = headers.get('Location', '')[len(domain):]
    assert actual_path == "/"


def test_post_login_success_auth_tkt_present(app, auth_env):
    response = app.post('/login', AUTH_DATA)
    headers = response.headers
    cookies_set = headers.getall("Set-Cookie")
    assert cookies_set
    for cookie in cookies_set:
        if cookie.startswith('auth_tkt'):
            break
    else:
        assert False


def test_post_login_fail(app, auth_env):
    data = {"username": "selemk", "password": "bob"}
    response = app.post('/login', data)
    assert response.status_code == 200


def test_post_login_fail_bad_password(app, auth_env):
    data = {"username": "seleniumk", "password": "bob"}
    response = app.post('/login', data)
    assert response.status_code == 200


def test_post_login_fail_bad_username(app, auth_env):
    data = {"username": "seumk", "password": "python"}
    response = app.post('/login', data)
    assert response.status_code == 200


def test_groupfinder(auth_env):
    from learning_journal.security import groupfinder
    assert groupfinder('seleniumk', {}) == ['group:users']

