"""
This webserver translates http get requestes
into select satements for a MariaDB#

@autor Maximilian Hartmann
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import mysql.connector as mariaDB
from urllib.parse import urlparse
from urllib.parse import unquote
from pathlib import Path
import itertools
import json




hostName = "localhost"
serverPort = 42030
#is the serverclass
class MyServer(BaseHTTPRequestHandler):
    #decyphers the request
    def do_GET(self):
        
        chopped_self = urlparse(self.path)
        
        
        if chopped_self.path == '/':
            MyServer.serv_test(self)
        elif chopped_self.path =='/modules':
            MyServer.serv_module(self)
        elif chopped_self.path =='/user':
            MyServer.serv_user(self)
        elif chopped_self.path =='/answers':
            MyServer.serv_answers(self)
        elif chopped_self.path =='/user':
            MyServer.serv_user(self)
        elif chopped_self.path =='/tasks':
            MyServer.serv_tasks(self)
        elif chopped_self.path =='/user_module':
            MyServer.serv_user_module(self)
        else:
            print(chopped_self.path)
            self.send_error(404)
            print('dummy')

        print(self.client_address)
        print(self.path)

    #is called if no section is given
    def serv_test(self):
        print('SERVING module 200')
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes("This is a Test", "utf-8"))
        print(self.client_address)
    #serves modules
    def serv_module(self):
        print("modul_serv-----------------------------------------------------------------")

        chopped_self = urlparse(self.path)
        print(chopped_self)
        try:
            if (chopped_self.query):
                query_self = unquote(chopped_self.query)
                print("Querry______Funoo")
                print(query_self)
                query_dict = dict(qc.split("=") for qc in query_self.split("&"))
                print( query_dict)
                #building the select statemanet
                select_string = "SELECT * FROM modules WHERE "
                replyJSON = MyServer.execute_select(select_string + MyServer.build_select_string(query_dict))
            else:
                replyJSON = MyServer.execute_select('SELECT * FROM modules;')
                print("hi")
            print('SERVING module 200')
            self.send_response(200)
            self.send_header("Content-type", "JSON")
            self.end_headers()
            self.wfile.write(bytes(replyJSON, "utf-8"))
            print(self.client_address)
        except:
            print("send_error")
            self.send_error(404)
    #serves users
    def serv_user(self):
        print("User_serv-----------------------------------------------------------------")
        chopped_self = urlparse(self.path)
        print(chopped_self)
        try:
            if (chopped_self.query):
                query_self = unquote(chopped_self.query)
                query_dict = dict(qc.split("=") for qc in query_self.split("&"))
                print( query_dict)
                #building the select statemanet
                select_string = "SELECT * FROM user WHERE "
                replyJSON = MyServer.execute_select(select_string + MyServer.build_select_string(query_dict))
            else:
                print("hi")
                replyJSON = MyServer.execute_select('SELECT * FROM user;')
            print(type(replyJSON))    
            print('SERVING User 200')
            self.send_response(200)
            self.send_header("Content-type", "JSON")
            self.end_headers()
            self.wfile.write(bytes(replyJSON, "utf-8"))
            print(self.client_address)
        except:
            print("send_error")
            self.send_error(404)
    #serves answers
    def serv_answers(self):
        print("answer_serv-----------------------------------------------------------------")
        chopped_self = urlparse(self.path)
        print(chopped_self)
        try:
            if (chopped_self.query):
                query_self = unquote(chopped_self.query)
                query_dict = dict(qc.split("=") for qc in query_self.split("&"))
                print( query_dict)
                #building the select statemanet
                select_string = "SELECT * FROM answers WHERE "
                replyJSON = MyServer.execute_select(select_string + MyServer.build_select_string(query_dict))
            else:
                replyJSON = MyServer.execute_select('SELECT * FROM answers;')
                print("hi")
            print('SERVING module 200')
            self.send_response(200)
            self.send_header("Content-type", "JSON")
            self.end_headers()
            self.wfile.write(bytes(replyJSON, "utf-8"))
            print(self.client_address)
        except:
            print("send_error")
            self.send_error(404)
    #serves tasks
    def serv_tasks(self):
        print("tasks_serv-----------------------------------------------------------------")
        chopped_self = urlparse(self.path)
        print(chopped_self)
        try:
            if (chopped_self.query):
                query_self = unquote(chopped_self.query)
                query_dict = dict(qc.split("=") for qc in query_self.split("&"))
                print( query_dict)
                #building the select statemanet
                select_string = "SELECT * FROM tasks WHERE "
                replyJSON = MyServer.execute_select(select_string + MyServer.build_select_string(query_dict))
            else:
                replyJSON = MyServer.execute_select('SELECT * FROM tasks;')
                print("hi")
            print('SERVING module 200')
            self.send_response(200)
            self.send_header("Content-type", "JSON")
            self.end_headers()
            self.wfile.write(bytes(replyJSON, "utf-8"))
            print(self.client_address)
        except:
            print("send_error")
            self.send_error(404)
    #serves the user module
    def serv_user_module(self):
        print("user_module_serv-----------------------------------------------------------------")
        chopped_self = urlparse(self.path)
        print(chopped_self)
        try:
            if (chopped_self.query):
                query_self = unquote(chopped_self.query)
                query_dict = dict(qc.split("=") for qc in query_self.split("&"))
                print( query_dict)
                #building the select statemanet
                select_string = "SELECT * FROM user_module WHERE "
                replyJSON = MyServer.execute_select(select_string + MyServer.build_select_string(query_dict))
            else:
                replyJSON = MyServer.execute_select('SELECT * FROM user_module;')
                print("hi")
            print('SERVING module 200')
            self.send_response(200)
            self.send_header("Content-type", "JSON")
            self.end_headers()
            self.wfile.write(bytes(replyJSON, "utf-8"))
            print(self.client_address)
        except:
            print("send_error")
            self.send_error(404)

    #is called if a section, that not exists is called
    def section_not_found():
        self.send_error(404)
        print('SECTION NOT FOUND ERROR 404')
        
    #exicutes a select on our MariaDB
    def execute_select(selcetString):

        # connect to the mariaDB

        con = mariaDB.connect(host='192.168.2.168', user = 'development',password='dev',database='naoworks')

        # Exicute SQL command
        cursor = con.cursor()
        SQLBefehl = selcetString
        cursor.execute(SQLBefehl)
        desc=cursor.description
        #put results into dictionarys
        listOfDicts = []
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

    #builds the where part of a select statement
    def build_select_string(query_dict):
        i = 0
        select_string =''
        for key in query_dict:
            print("in Key Value loop")
            if (i != 0):
                select_string = select_string + " AND "
            select_string = select_string + key + " = " +"'" + query_dict[key].replace('%20',' ') + "'"
            i=+ 1
        select_string = select_string + ";"
        print (select_string)
        return select_string

#initializes the Webserver
if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")