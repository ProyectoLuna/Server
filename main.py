#!/usr/bin/env python3


import time
import sqlite3
import json

from http.server import BaseHTTPRequestHandler, HTTPServer

db = "db.sqlite"


def dict_factory(cursor, row):
    """ Creates dictionaries from sqlite queries """
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


# HTTPRequestHandler class
class LunaHTTPServer_RequestHandler(BaseHTTPRequestHandler):
    # OPTIONS
    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Credentials', 'true')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With, Content-type")
        self.end_headers()

    # GET

    def do_GET(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        if self.path == "/check/":
            self.wfile.write(bytes("OK", "UTF-8"))
            return

        return

    # POST

    def do_POST(self):

        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        # Client

        if self.path == "/client-create/":
            self.wfile.write(bytes("OK", "UTF-8"))
            return
        return


def main():
    print('{0} : Server starting'.format(time.asctime()))

    # Server settings
    server_address = ('0.0.0.0', 8081)
    httpd = HTTPServer(server_address, LunaHTTPServer_RequestHandler)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt as e:
        httpd.server_close()
        print(e)
        print('{0} : Server stops'.format(time.asctime()))


if __name__ == "__main__":
    main()
