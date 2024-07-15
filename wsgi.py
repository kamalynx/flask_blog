#!/usr/bin/env python3
from app import create_app
from waitress import serve

app = create_app()

if __name__ == '__main__':
    serve(app, unix_socket='/tmp/waitress.sock', unix_socket_perms='666')
