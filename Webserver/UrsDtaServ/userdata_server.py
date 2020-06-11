# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
from urllib.parse import urlparse


hostName = "localhost"
serverPort = 42030

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        fun = self
        MyServer.section_switcher(fun)
        """
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes("test", "utf-8"))
        """
        print(self.client_address)
        print(self.path)

    def section_switcher(fun):
        argument = urlparse(fun.path)
        switcher={
            '/modules': MyServer.serv_modules,
             '/test': MyServer.serv_test
            }
        func = switcher.get(argument.path, lambda: section_not_found())
        return func(fun)

    def serv_test(self):
        print('SERVING TEST 200')
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes("test", "utf-8"))
        print(self.client_address)
        print(self.path)

    def serv_modules(self):
        print('SERVING TEST 200')
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes("modules", "utf-8"))
        print(self.client_address)
        print(self.path)

    def section_not_found():
        print('SECTION NOT FOUND ERROR 404')
        
         




if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")