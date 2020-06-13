# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import mysql.connector as mariaDB
from urllib.parse import urlparse
from pathlib import Path
import itertools
import json




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
        elif chopped_self.path =='/users':
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
        path = Path(__file__).parent / "module1.json"
        file_to_open = open(path).read()
        chopped_self = urlparse(self.path)
        print(chopped_self)
        if (chopped_self.query):
            query_self = chopped_self.query
            query_dict = dict(qc.split("=") for qc in query_self.split("&"))
            print( query_dict)
            #building the select statemanet
            select_string = "SELECT * FROM modules WHERE "
            print (select_string)
            i = 0
            for key in query_dict:
                print("in Key Value loop")
                if (i != 0):
                    select_string = select_string + " AND "
                select_string = select_string + key + " = " +"'" + query_dict[key] + "'"
                i=+ 1
            select_string = select_string + ";"
            print (select_string)
            replyJSON = MyServer.execute_select(select_string)

        print('SERVING modules 200')
        self.send_response(200)
        self.send_header("Content-type", "JSON")
        self.end_headers()
        self.wfile.write(bytes(replyJSON, "utf-8"))
        print(self.client_address)
        print(self.path)
    """try:
            path = Path(__file__).parent / "module1.json"
            file_to_open = open(path).read()
            chopped_self = urlparse(self.path)
            print(chopped_self)
            if (chopped_self.query):
                query_self = chopped_self.query
                query_dict = dict(qc.split("=") for qc in query_self.split("&"))
                print( query_dict)
                #building the select statemanet
                select_string = "SELECT * FROM modules WHERE "
                print (select_string)
                i = 0
                for key in query_dict:
                    print("in Key Value loop")
                    if (i != 0):
                        select_string = select_string + " AND "
                    select_string = select_string + key + " = " + query_dict[key]
                    i=+ 1
                print (select_string)
                MyServer.execute_select(select_string)

            print('SERVING modules 200')
            self.send_response(200)
            self.send_header("Content-type", "JSON")
            self.end_headers()
            self.wfile.write(bytes(file_to_open, "utf-8"))
        except:
            print("send_error")
            self.send_error(404)
      """
      
    def serv_users(self):
        print('SERVING USRS 200')
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes("Users", "utf-8"))
        print(self.client_address)
        print(self.path)

    def section_not_found():

        print('SECTION NOT FOUND ERROR 404')
        
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
        print("testing fetch all-----------------------------------------")
        #testerg = test.fetchall()
        #for x in testerg:
            #print (x)
        print("end of fetch test-----------------------------------------")
        print("ioudehasfgiuosdfghiöh")
        print(cursor.description)
        desc=cursor.description
        print(type(desc[0]))
        print("=-=-=-=-=")

        listOfDicts = []
        # Durchlaufen der Ergebnisse
        row=cursor.fetchone()

        while (row!=None):
            print(row)
            i = len(row)
            i-=1
            tempdict={}
            while i >= 0:
                if(row[i]):
                    print(row[i])
                    tempdict.update({desc[i][0] : row[i].__str__()})
                i-=1
            listOfDicts.append(tempdict)
            row = cursor.fetchone()
        print(listOfDicts)
        # Ende der Verarbeitung
        cursor.close()
        # Abmelden
        con.disconnect()
        return json.dumps(listOfDicts)

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