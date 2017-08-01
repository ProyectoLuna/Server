import ssl
import logging
from pathlib import Path

from customlog.customlog import ColoredLogger
from certificate.certificate import create_self_signed_cert

from twisted.web import server
from twisted.internet import reactor, endpoints, ssl

from server import ServerHandler


def main():

    logging.setLoggerClass(ColoredLogger)
    logger = logging.getLogger('SERVER - MAIN')
    cacert = "cacert.pem"
    privkey = "privkey.pem"

    # Check if certifice exists
    cacert_file = Path(cacert)
    privkey_file = Path(privkey)

    if not cacert_file.is_file() or not privkey_file.is_file():
        create_self_signed_cert(cacert, privkey)

    server_port = 8080

    ssl_context = ssl.DefaultOpenSSLContextFactory(
        privkey,
        cacert,
    )

    site = server.Site(ServerHandler())
    endpoint = endpoints.SSL4ServerEndpoint(reactor, server_port, ssl_context)
    endpoint.listen(site)

    logger.info('Server start listening on {0}'.format(server_port))
    reactor.run()


if __name__ == '__main__':
    main()
