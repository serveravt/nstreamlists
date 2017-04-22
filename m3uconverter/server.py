#!/usr/bin/env python

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import os, converter

#Create custom HTTPRequestHandler class
class KodeFunHTTPRequestHandler(BaseHTTPRequestHandler):

    #handle GET command
    def do_GET(self):
        rootdir = '.' #file location
        try:
            if 'getlist' in self.path:
                converter.convert()
                f = open(rootdir + "/output.xml") #open requested file
                #send code 200 response
                self.send_response(200)

                #send header first
                self.send_header('Content-type','application/xml')
                self.end_headers()

                #send file content to client
                self.wfile.write(f.read());
                f.close()
                return

        except IOError:
            self.send_error(404, 'file not found')

def run():
    print('http server is starting...')
    server_address = ('0.0.0.0', 1025)
    httpd = HTTPServer(server_address, KodeFunHTTPRequestHandler)
    print('http server is running...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
