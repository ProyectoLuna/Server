import ssl
import logging

from customlog.customlog import ColoredLogger

from twisted.web import server
from twisted.internet import reactor, endpoints, ssl

from server import ServerHandler


def main():

    logging.setLoggerClass(ColoredLogger)
    logger = logging.getLogger('SERVER - MAIN')

    server_port = 8080

    ssl_context = ssl.DefaultOpenSSLContextFactory(
        'privkey.pem',
        'cacert.pem',
    )

    site = server.Site(ServerHandler())
    endpoint = endpoints.SSL4ServerEndpoint(reactor, server_port, ssl_context)
    endpoint.listen(site)

    logger.info('Server start listening on {0}'.format(server_port))
    reactor.run()


if __name__ == '__main__':
    main()
