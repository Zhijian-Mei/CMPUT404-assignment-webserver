#  coding: utf-8
import re
import socketserver
import os
from os import path


# Copyright 2022 Zhijian Mei
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024).strip()
        # print("Got a request of: %s\n" % self.data)

        requests = self.data.splitlines()
        for index, item in enumerate(requests):
            print(index, item)
        host = requests[1].decode('utf-8').split(" ")

        ret = re.match("GET", requests[0].decode('utf-8'))
        if not ret:
            response = "HTTP/1.1 405 Method Not Allowed\r\n"
            response += "\r\n"
            self.request.sendall(bytearray(response, 'utf-8'))
            return
        ret = re.match(r"[^/]+(/[^ ]*)", requests[0].decode('utf-8'))
        if ret:
            file_name = ret.group(1)
            # print("*" * 50, file_name)

        file_name = file_name[1:]
        # print("*" * 50, file_name)


        try:
            assert (not re.match("../",file_name))
            file_path = "./www/" + file_name
            if path.isdir(file_path):
                if file_path[-1] != "/":

                    response = "HTTP/1.1 301 Moved Permanently\r\n"
                    response += "Location: " + "/" + file_name + "/\r\n"
                    response += "\r\n"

                    self.request.sendall(bytearray(response, 'utf-8'))
                    return
                file_path = file_path + "index.html"

                f = open(file_path, "rb")
            else:

                f = open(file_path, "rb")
        except:
            response = "HTTP/1.1 404 NOT FOUND\r\n"
            response += "\r\n"
            self.request.sendall(bytearray(response, 'utf-8'))
        else:
            content = f.read()
            f.close()

            response = "HTTP/1.1 200 OK\r\n"
            file = path.splitext(file_path)
            filename, type = file
            if type == ".css":
                response += "Content-Type: text/css\r\n"
            if type == ".html":
                response += "Content-Type: text/html\r\n"
            response += "\r\n"
            self.request.sendall(bytearray(response, 'utf-8'))
            self.request.sendall(bytearray(content))


    # def css(self,file_name):


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
