LOG_FILE = 'log.log'
HOST, PORT = "50.0.0.2", 514

import logging
import socketserver

logging.basicConfig(level=logging.DEBUG, format='%(message)s', datefmt='', filename=LOG_FILE, filemode='a')


class SyslogUDPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data = bytes.decode(self.request[0].strip())
        socket = self.request[1]
        print( str(self.client_address[0]) + ": " + str(data))
        logging.debug(str(data))


if __name__ == "__main__":
    try:
        server = socketserver.UDPServer((HOST, PORT), SyslogUDPHandler)
        server.serve_forever(poll_interval=0.5)
    except (IOError, SystemExit):
        raise
    except KeyboardInterrupt:
        print ("Crtl+C Pressed. Shutting down.")