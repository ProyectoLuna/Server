import sqlite3
import json
import logging

from twisted.web import resource


def dict_factory(cursor, row):
    """ Creates dictionaries from sqlite queries """
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class ServerHandler(resource.Resource):
    isLeaf = True

    def __init__(self):
        super(ServerHandler, self).__init__()
        self.db = "db.sqlite"
        self.logger = logging.getLogger("SERVER - HANDLER")

    def render(self, request):
        self.logger.debug("From {0} Got {1} Request"
                          .format(request.getClientIP(),
                                  request.method.decode("UTF-8")))

        if request.method == b"OPTIONS":
            request.setHeader(b'Access-Control-Allow-Credentials', b'true')
            request.setHeader(b'Access-Control-Allow-Credentials', b'true')
            request.setHeader(b'Access-Control-Allow-Origin', b'*')
            request.setHeader(b'Access-Control-Allow-Methods', b'GET, POST, OPTIONS')
            request.setHeader(b'Access-Control-Allow-Headers', b'X-Requested-With, Content-type')

        if request.method == b"GET":

            if request.uri == b"/check_server":

                request.setHeader(b"content-type", b"application/json")
                data = bytes(200)
                return data

            elif request.uri == b"/check_gateway":

                with sqlite3.connect(self.db) as conn:
                    conn.row_factory = dict_factory
                    cursor = conn.cursor()
                    cursor.execute("SELECT * FROM gateway")
                    query = cursor.fetchall()

                request.setHeader(b"content-type", b"application/json")
                data = bytes(json.dumps(query), "UTF-8")
                return data

            elif request.uri == b"/check_zones":
                with sqlite3.connect(self.db) as conn:
                    conn.row_factory = dict_factory
                    cursor = conn.cursor()
                    cursor.execute("SELECT * FROM zones")
                    query = cursor.fetchall()
                request.setHeader(b"content-type", b"application/json")
                data = bytes(json.dumps(query), "UTF-8")
                self.logger.debug(data)
                return data

        elif request.method == b"POST":

            if request.uri == b"/auth":

                json_data = request.content.read()
                rdata = json.loads(json_data.decode("UTF-8"))

                with sqlite3.connect(self.db) as conn:
                    conn.row_factory = dict_factory
                    cursor = conn.cursor()
                    cursor.execute("SELECT * FROM users WHERE username = ?", (rdata['user'],))
                    query = cursor.fetchone()

                message = {'auth': False}

                if query:
                    if rdata['pass'] == query['password']:
                        message = {'auth': True}

                wdata = bytes(json.dumps(message), "UTF-8")
                request.setHeader(b"content-type", b"application/json")
                return wdata

        return b"NONONONONO"
