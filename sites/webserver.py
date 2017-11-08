import SimpleHTTPServer
import SocketServer
import socket

from argparse import ArgumentParser
parser = ArgumentParser(description="Webserver")


class CS144Handler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    # Disable logging DNS lookups
    def address_string(self):
        return str(self.client_address[0])

parser.add_argument('--tfo',
                    type=bool,
                    help="enables tfo",
                    default=False)

# Expt parameters
args = parser.parse_args()

PORT = 80
Handler = CS144Handler
httpd = SocketServer.TCPServer(("", PORT), Handler)
print "Server1: httpd serving at port", PORT

if (args.tfo):
  httpd.socket.setsockopt(socket.SOL_TCP, 23, 5)

#httpd.socket.setsockopt(socket.SOL_TCP, 23, 5)
#httpd.socket.setsockopt(socket.SOL_TCP)
#httpd.socket.setsockopt()
#httpd.socket
httpd.serve_forever()
