import os

from fabric.api import run
from fabric.context_managers import settings, shell_env

server = os.environ.get('SERVER')
port = os.environ.get('PORT')

"""
Run like this: SERVER=192.168.0.1 PORT=22 STAGING_SERVER=stage-superlists.richardnpaul.co.uk ./manage.py test functional_tests.test_my_lists
"""


def _get_manage_dot_py(host):
    return f'~/sites/{host}/virtualenv/bin/python ~/sites/{host}/manage.py'

def reset_database(host):
    manage_dot_py = _get_manage_dot_py(host)
    with settings(host_string=f'richard@{server}:{port}'):
        run(f'{manage_dot_py} flush --noinput')

def _get_server_env_vars(host):
    env_lines = run(f'cat ~/sites/{host}/.env').splitlines()
    return dict(l.split('=') for l in env_lines if l)

def create_session_on_server(host, email):
    manage_dot_py = _get_manage_dot_py(host)
    with settings(host_string=f'richard@{server}:{port}'):
        env_vars = _get_server_env_vars(host)
        with shell_env(**env_vars):
            session_key = run(f'{manage_dot_py} create_session {email}')
            return session_key.strip()
