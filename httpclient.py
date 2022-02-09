#!/usr/bin/env python3
# coding: utf-8
# Copyright 2022 Abram Hindle, Jason Branch-Allen https://github.com/tywtyw2002, and https://github.com/treedust
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

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it



''' 
CITATIONS AND SOURCES

Cev. (2011, January 13). Parse raw HTTP headers. Stack Overflow. Retrieved February 9, 2022, from https://stackoverflow.com/questions/4685217/parse-raw-http-headers/5955949. Answered By: Brandon Rhodes(2011, May 10)

Urllib.parse - parse urls into components¶. urllib.parse - Parse URLs into components - Python 3.10.2 documentation. (n.d.). Retrieved February 9, 2022, from https://docs.python.org/3/library/urllib.parse.html#module-urllib.parse

7. input and output¶. 7. Input and Output - Python 3.10.2 documentation. (n.d.). Retrieved February 9, 2022, from https://docs.python.org/3/tutorial/inputoutput.html

user1814720. (2017, December 5). Implementing HTTP client with sockets (without HTTP libraries) with python. Stack Overflow. Retrieved February 9, 2022, from https://stackoverflow.com/questions/47658584/implementing-http-client-with-sockets-without-http-libraries-with-python. Answered By: t.m.adam(2017, December 5)

dsclose. (n.d.). Using Python's socket module to send HTTP requests and receive the response. Gist. Retrieved February 9, 2022, from https://gist.github.com/dsclose/bf0557e3e80ff7d66696

user1289853. (2012, May 5). Sending "user-agent" Using requests library in python. Stack Overflow. Retrieved February 9, 2022, from https://stackoverflow.com/questions/10606133/sending-user-agent-using-requests-library-in-python. Answered By: 逆さま(2012, May 15)

CuriousGuy. (2017, August 15). Send RAW POST request using socket. Stack Overflow. Retrieved February 9, 2022, from https://stackoverflow.com/questions/45695168/send-raw-post-request-using-socket. Answered By: sauerburger(2017, August 22)

saturn99. (n.d.). Post HTTP python socket. Gist. Retrieved February 9, 2022, from https://gist.github.com/saturn99/5e85a100d695dcbd343459d9906f285a

Socket - low-level networking interface¶. socket - Low-level networking interface - Python 3.10.2 documentation. (n.d.). Retrieved February 9, 2022, from https://docs.python.org/3/library/socket.html

Post - http: MDN. HTTP | MDN. (n.d.). Retrieved February 9, 2022, from https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST

HTTP request methods. HTTP Methods GET vs POST. (n.d.). Retrieved February 9, 2022, from https://www.w3schools.com/tags/ref_httpmethods.asp

zakdances. (2011, October 25). Python: Get url path sections. Stack Overflow. Retrieved February 9, 2022, from https://stackoverflow.com/questions/7894384/python-get-url-path-sections. Answered By: Josh Lee(2011, October 25) 

CMPUT 404 Course Notes and Lab Exercises(2022)

'''



import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib.parse


def help():
    print("httpclient.py [GET/POST] [URL]\n")


class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body


class HTTPClient(object):
    # def get_host_port(self,url):

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        print("Socket created successfully...")
        return None

    def get_code(self, data):
        code = int(data.split(' ')[1])
        return code

    def get_headers(self, data):
        return None

    def get_body(self, data):
        body = data.split('\r\n\r\n')[1]
        return body

    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))

    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    def GET(self, url, args=None):

        # Get Path, Host, and Port
        request_path = self.get_path(url)
        host = self.get_host(url)
        port = self.get_port(url)

        self.connect(host, port)

        get_headers = (
            f'GET {request_path} HTTP/1.1\r\n'
            f'Host: {host}\r\n'
            f'User-Agent: Mozilla/5.0\r\n'
            f'Connection: close\r\n\r\n' 
        )

        # Send the headers
        self.sendall(get_headers)
        send_response = self.recvall(self.socket)
        self.close()

        response_code = self.get_code(send_response)
        response_body = self.get_body(send_response)

        # Print Response
        lineBreak = '\n' + '-'*80 + '\n'
        printedResponse = lineBreak + '\n' + send_response + lineBreak

        print(printedResponse)


        return HTTPResponse(response_code, response_body)

    def POST(self, url, args=None):
        body = ""

        if args != None:
            body = urllib.parse.urlencode(args)
        
        content_length = len(body)

        # Get Path, Host, and Port
        request_path = self.get_path(url)
        host = self.get_host(url)
        port = self.get_port(url)

        self.connect(host, port)

        post_headers = (
            f'POST {request_path} HTTP/1.1\r\n'
            f'Host: {host}\r\n'
            f'User-Agent: Mozilla/5.0\r\n'
            f'Accept: */*\r\n'
            f'Content-Type: application/x-www-form-urlencoded\r\n'
            f'Content-Length: {content_length}\r\n'
            f'Connection: closed\r\n\r\n'
            f'{body}'
        )

         # Send the headers
        self.sendall(post_headers)
        send_response = self.recvall(self.socket)
        self.close()

        response_code = self.get_code(send_response)
        response_body = self.get_body(send_response)

        # Print Response
        lineBreak = '\n' + '-'*80 + '\n'
        printedResponse = lineBreak + '\n' + send_response + lineBreak

        print(printedResponse)

        return HTTPResponse(response_code, response_body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST(url, args)
        else:
            return self.GET(url, args)

    def get_path(self, url):
        parseURL = urllib.parse.urlparse(url)

        if parseURL.path:
            path = parseURL.path
        else:
            path = '/'

        return path

    def get_host(self, url):
        parseURL = urllib.parse.urlparse(url)
        host = parseURL.hostname
        return host

    def get_port(self, url):
        parseURL = urllib.parse.urlparse(url)

        if parseURL.port != None:
            port = parseURL.port
        else:
            port = 80

        return port


if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command(sys.argv[2], sys.argv[1]))
    else:
        print(client.command(sys.argv[1]))
