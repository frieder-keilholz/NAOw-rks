# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
from urllib.parse import urlparse


hostName = "localhost"
serverPort = 42030

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        
        chopped_self = urlparse(self.path)
        print(chopped_self)
        
        if chopped_self.path == '/':
            MyServer.serv_test(self)
        elif chopped_self.path =='/modules':
            MyServer.serv_modules(self)
        else:
            print(chopped_self.path)
            #self.send_response(404)
            #self.end_headers()
            #self.wfile.write(bytes("404", "utf-8"))
            self.send_error(404)
            print('dummy')

        print(self.client_address)
        print(self.path)


    def serv_test(self):
        print('SERVING TEST 200')
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes("test", "utf-8"))
        print(self.client_address)
        print(self.path)

    def serv_modules(self):
        file_to_open = open("D:\\vs_repos\\nao_wrks\\Webserver\\UrsDtaServ\\module1.json").read()
        try:
            
            print('SERVING modules 200')
            self.send_response(200)
            self.send_header("Content-type", "JSON")
            self.end_headers()
            self.wfile.write(bytes(file_to_open, "utf-8"))
        except:
            self.send_error(404)

        print(self.client_address)
        print(self.path)

    def section_not_found():
        print('SECTION NOT FOUND ERROR 404')
        
#code for query work
"""
query_self = chopped_self.query
        query_dict = dict(qc.split("=") for qc in query_self.split("&"))
        print( query_dict)
"""



if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")