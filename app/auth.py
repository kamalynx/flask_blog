from flask import current_app as app
from flask_httpauth import HTTPDigestAuth

auth = HTTPDigestAuth()


@auth.get_password
def get_pw(username):
    users = app.config.get('USERS')

    if users is not None and username in username:
        return users.get(username)
    return
