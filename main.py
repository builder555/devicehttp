from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class DeviceHTTPWrapper:

    def __init__(self, device, http_port=8080, http_host='0.0.0.0'):
        Handler = HTTPRequestHandler
        Handler.device = device
        config = (http_host, http_port)
        self.server = HTTPServer(config, Handler)

    def start(self):
        self.server.serve_forever()

    def shutdown(self):
        self.server.shutdown()


class HTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_ok_response({'output': self.device.is_on})

    def do_POST(self):
        try:
            if self.json_data['on']:
                self.device.start()
            else:
                self.device.stop()
            self.send_ok_response()
        except:
            self.send_error_response()

    def log_request(self, *a, **kw): # this is to silence the http.server logs
        return
    
    def send_error_response(self):
        self.send_response(400)
        self.end_headers()

    def send_ok_response(self, data=None):
        self.send_response(200)
        self.end_headers()
        if data is not None:
            self.wfile.write(bytes(json.dumps(data),'utf-8'))

    @property
    def json_data(self):
        length = int(self.headers['Content-Length'])
        data = json.loads(self.rfile.read(length).decode('utf-8'))
        return data
