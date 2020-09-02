from http.server import BaseHTTPRequestHandler, HTTPServer
from request_handler import StatisticRequestHandler
import ipaddress
import logging
import json

class Reporter:
  def __init__(self, host, port):
    self.port = port
    ip_address = ipaddress.ip_address(host)
    if (ip_address.version == 4):
      self.ipv4 = host
    elif (ip_address.version == 6):
      self.ipv6 = host

def MakeStatisticServerWithArgv(request_handler):
  class StatisticServer(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
      self.request_handler = request_handler 
      super().__init__(request, client_address, server)

    def _set_headers(self):
      self.send_response(200)
      self.send_header('Content-Type', 'application/json')
      self.send_header('Access-Control-Allow-Origin', '*')
      self.end_headers()

    def do_POST(self):
      content_length = int(self.headers['Content-Length'])
      post_data = json.loads(self.rfile.read(content_length))
      logging.debug("%s" % post_data)
      (host,port) = self.client_address
      reporter = Reporter(host, port)
      request_handler.submitNewStatistic(reporter, post_data)
      self._set_headers()
      return

  return StatisticServer

if __name__ == "__main__":
  logging.basicConfig(format='%(levelname)s   %(asctime)s   %(message)s', level=logging.DEBUG)

  request_handler = StatisticRequestHandler()
  statistic_server = MakeStatisticServerWithArgv(request_handler)
  server_address = ('', 6789)
  httpd = HTTPServer(server_address, statistic_server)
  logging.debug("Start server: %s:%d"% server_address)
  httpd.serve_forever()