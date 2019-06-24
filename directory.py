#/usr/bin/env python3
import docker
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler

def href_for_port(port_data):
    # port is like {'8989/tcp': [{'HostIp': '0.0.0.0', 'HostPort': '8989'}]}
    host_ports = []
    for container, host in port_data.items():
        for host_thing in host:
            host_ports.append(host_thing['HostPort'])
    if len(host_ports) == 0:
        return 'none'
    else:
        return ', '.join([f'<a href="/" onclick="javascript:event.target.port={port}">{port}</a>' for port in host_ports])

class HTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        front_part = '''
        <html>
         <head>
          <title>Currently running services</title>
          <style>
           table {
             border: 1px solid #1C6EA4;
             background-color: #EEEEEE;
             text-align: left;
             border-collapse: collapse;
             margin-left: auto;
             margin-right: auto;
           }
           table td, table.blueTable th {
             border: 1px solid #AAAAAA;
             padding: 3px 2px;
           }
           table tr:nth-child(even) {
             background: #E6EEF5;
           }
           table thead {
             background: #1C6EA4;
             background: -moz-linear-gradient(top, #5592bb 0%, #327cad 66%, #1C6EA4 100%);
             background: -webkit-linear-gradient(top, #5592bb 0%, #327cad 66%, #1C6EA4 100%);
             background: linear-gradient(to bottom, #5592bb 0%, #327cad 66%, #1C6EA4 100%);
             border-bottom: 2px solid #444444;
           }
           table thead th {
             font-weight: bold;
             color: #FFFFFF;
             border-left: 2px solid #D0E4F5;
           }
           table thead th:first-child {
             border-left: none;
           }

           table tfoot td {
             font-size: 14px;
           }
           table tfoot .links {
             text-align: right;
           }
           table tfoot .links a{
             display: inline-block;
             background: #1C6EA4;
             color: #FFFFFF;
             padding: 2px 8px;
             border-radius: 5px;
           }
          </style>
         </head>
         <body>
          <table>
           <tr>
            <th>Name</th>
            <th>Port</th>
           </tr>
        '''
        back_part = '''
          </table>
         </body>
        </html>
        '''
        dclient = docker.from_env()
        middle_part = '\n'.join([f'<tr><td>{container.name}</td><td>{href_for_port(container.ports)}</td></tr>' for container in dclient.containers.list()])
        dclient.close()
        response = bytes(front_part + middle_part + back_part, 'UTF8')
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', len(response))
        self.end_headers()
        self.wfile.write(response)

if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s: %(asctime)-15s : %(lineno)s : %(message)s', level=logging.DEBUG)
    port = 80
    server_address = ('', port)
    httpd = HTTPServer(server_address, HTTPHandler)
    logging.info(f'Listening on :{port}')
    httpd.serve_forever()

