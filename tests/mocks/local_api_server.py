import json
import re
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

from .mock_mnubo_backend import MockMnuboBackend
from .routes import ROUTES


class LocalApiRequestHandler(BaseHTTPRequestHandler):
    def _send_response(self, body):

        self.wfile.write(body.encode('utf8'))

    def _get_route(self, method, path):
        for route, handler in ROUTES[method].items():
            matches = re.search(route, path)
            if matches:
                return handler, matches.groups()
        raise ValueError

    def _handle(self, method, path):
        if path.startswith('/api/v3'):
            path = path[7:]

        try:
            handler, matches = self._get_route(method, path)
        # no route defined
        except ValueError:
            self.send_error(404)
            return

        compress = path.startswith("/compress")

        if method == 'GET':
            code, resp_content = handler(self.server.backend, matches)
        else:
            length = int(self.headers['content-length'])
            content_type = self.headers['content-type']
            body = self.rfile.read(length) if length else "{}"

            if not compress and content_type == 'application/json':
                body = json.loads(body)

            code, resp_content = handler(self.server.backend, body, matches)

        self.send_response(code)
        if code < 300:
            self.send_header('Content-type', 'application/json')
            if compress:
                self.send_header('Content-encoding', 'gzip')
            self.end_headers()
            if resp_content is not None:
                if not compress:
                    resp_content = json.dumps(resp_content)
                self._send_response(resp_content)
        else:
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            if resp_content is not None:
                self._send_response(resp_content)

    def do_GET(self):
        self._handle('GET', self.path)

    def do_POST(self):
        self._handle('POST', self.path)

    def do_PUT(self):
        self._handle('PUT', self.path)

    def do_DELETE(self):
        self._handle('DELETE', self.path)

    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()


class LocalApiServer(object):
    def __init__(self):
        self.server = HTTPServer(("localhost", 0), LocalApiRequestHandler)
        self.server.backend = MockMnuboBackend()

        self.thread = threading.Thread(target=self.server.serve_forever)
        self.thread.daemon = True

    def start(self):
        self.thread.start()
        print("started local API server at", self.path)

    def stop(self):
        self.server.shutdown()
        self.thread.join()
        print("stopped local API")

    @property
    def path(self):
        return "http://localhost:{}".format(self.server.server_port)


if __name__ == '__main__':
    server = LocalApiServer()
    # print ROUTES

    server.start()

    try:
        while True:
            pass

    except KeyboardInterrupt:
        pass

    server.stop()
