# Python 3 server for the nao
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import mysql.connector as mariaDB
from urllib.parse import urlparse
import json

hostName = "localhost"
serverPort = 42031

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        chopped_self = urlparse(self.path)
        print(chopped_self)
        if chopped_self.path == '/':
            MyServer.serv_test(self)
        elif chopped_self.path == '/modulerq':
            MyServer.serv_modulpackage(self)
        else:
            print(chopped_self.path)
            self.send_error(404)
            print('dummy')

    def serv_test(self):
        print('SERVING Test 200')
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes("This is a Test", "utf-8"))
        print(self.client_address)

    def serv_modulpackage(self):
        print("modulPackage_serv-----------------------------------------------------------------")
        chopped_self = urlparse(self.path)
        print(chopped_self)
        if (chopped_self.query):
            print("yeet")
            query_dict = dict(qc.split("=") for qc in chopped_self.query.split("&"))
            module_id_dict= json.loads(MyServer.execute_select(" SELECT module_id FROM nao_module_assignment WHERE nao_id = '" + query_dict["nao_id"] +"'" +';'))[0]
            print(module_id_dict)
            module_dict = json.loads(MyServer.execute_select(" SELECT * FROM modules WHERE module_id = '" + module_id_dict['module_id'] +"'"+';'))[0]
            print(module_dict)
            tasks_dict = json.loads(MyServer.execute_select(" SELECT * FROM tasks WHERE module_id = '" + module_id_dict['module_id'] +"'" +';'))
            print (tasks_dict)
        else:
            print("send_error")
            self.send_error(400)
    def execute_select(selcetString):
        Servername = '192.168.2.168' 
        Benutzer   = 'development'
        Passwort   = 'dev'
        Datenbank  = 'naoworks'

        # connect to the mariaDB

        con = mariaDB.connect(host='192.168.2.168', user = 'development',password='dev',database='naoworks')

        # Exicute SQL command
        cursor = con.cursor()
        SQLBefehl = selcetString
        test = cursor.execute(SQLBefehl)

        desc=cursor.description
        
        listOfDicts = []
        # Durchlaufen der Ergebnisse
        row=cursor.fetchone()

        while (row!=None):
            i = len(row)
            i-=1
            tempdict={}
            while i >= 0:
                if(row[i]):
                    tempdict.update({desc[i][0] : row[i].__str__()})
                i-=1
            listOfDicts.append(tempdict)
            row = cursor.fetchone()
        cursor.close()
        # Abmelden
        con.disconnect()
        return json.dumps(listOfDicts)

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")