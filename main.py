#!/usr/bin/env python3


import time
import sqlite3
import json
import logging

from http.server import BaseHTTPRequestHandler, HTTPServer
from customlog.customlog import ColoredLogger

logging.setLoggerClass(ColoredLogger)
logger = logging.getLogger('SERVER - MAIN')

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

        if self.path == "/check_gateway/":
            self.wfile.write(bytes("OK", "UTF-8"))

            with sqlite3.connect(db) as conn:
                conn.row_factory = dict_factory
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM gateway")
                query = cursor.fetchall()

            data = bytes(json.dumps(query), "UTF-8")

            self.wfile.write(data)
            return

        return

    # POST

    def do_POST(self):

        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        # Client

        if self.path == "/subscriptor_create/":
            """
            var_len = int(self.headers['Content-Length'])
            json_data = self.rfile.read(var_len)
            data = json.loads(json_data.decode("UTF-8"))

            with sqlite3.connect(db) as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO clients VALUES (NULL, ?, ?, ?, ?, ?)",
                               (data["name"], data["surname"], data["tlf"], data["email"], data["nif"],))
                conn.commit()
            """
            return
        return


def main():

    # Server settings
    server_address = ('0.0.0.0', 8081)
    httpd = HTTPServer(server_address, LunaHTTPServer_RequestHandler)

    try:
        logger.info('Server starting listening on ({0})'.format(server_address))
        httpd.serve_forever()
    except KeyboardInterrupt as e:
        httpd.server_close()
        logger.info('Server stops')


if __name__ == "__main__":
    main()
