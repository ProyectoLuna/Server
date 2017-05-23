#!/usr/bin/env python3

import ssl
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

    def log_message(self, formatting, *args):
        logger.info("From {0[0]} - {1}".format(self.client_address, formatting % args))

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

        if self.path == "/check_gateway":

            with sqlite3.connect(db) as conn:
                conn.row_factory = dict_factory
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM gateway")
                query = cursor.fetchall()

            data = bytes(json.dumps(query), "UTF-8")
            self.wfile.write(data)
            logger.debug(data)
            return

        elif self.path == "/check_subscriptors":
            with sqlite3.connect(db) as conn:
                conn.row_factory = dict_factory
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM subscriptors")
                query = cursor.fetchall()

            data = bytes(json.dumps(query), "UTF-8")
            self.wfile.write(data)
            logger.debug(data)
            return

        return

    # POST
    def do_POST(self):

        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        if self.path == "/auth":
            var_len = int(self.headers['Content-Length'])
            json_data = self.rfile.read(var_len)
            rdata = json.loads(json_data.decode("UTF-8"))

            with sqlite3.connect(db) as conn:
                conn.row_factory = dict_factory
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM users WHERE username = ?", (rdata['user'],))
                query = cursor.fetchone()

            message = {'auth': False}
            if query:
                if rdata['pass'] == query['password']:
                    message = {'auth': True}

            wdata = bytes(json.dumps(message), "UTF-8")
            self.wfile.write(wdata)

            return

        elif self.path == "/subscriptor_create":
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
    server_address = ('0.0.0.0', 8080)
    httpd = HTTPServer(server_address, LunaHTTPServer_RequestHandler)
    httpd.socket = ssl.wrap_socket(httpd.socket, certfile='./server.pem', server_side=True)

    try:
        logger.info('Server start listening on {0[0]}:{0[1]}'.format(server_address))
        httpd.serve_forever()
    except KeyboardInterrupt as e:
        logger.info('Server stops')
        httpd.server_close()


if __name__ == "__main__":
    main()
