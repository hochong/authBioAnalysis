import http.server
import socketserver
import json

PORT = 12345

#modifying https://gist.github.com/mdonkers/63e115cc0c79b4f6b8b3a6b797e485c7
class serverResponseHandler(http.server.BaseHTTPRequestHandler):
    def setheader(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

    def do_GET(self):
        print("GET request received")
        self.setheader()
        self.wfile.write("<p>GET request received<p>".format(self.path).encode('utf-8'))

    def do_POST(self):
        print("POST request received")
        len = int(self.headers['Content-Length'])
        postData = self.rfile.read(len)
        print(str(postData.decode('utf8')))
        jsonData = json.loads(postData)
        print(jsonData)
        print("classifierSelection:" + jsonData["classifierSelection"])
        print("classifierList:" + str(jsonData["classifierList"]))
        print("inputDataSelection" + jsonData["inputDataSelection"])
        print("InputDataList" + str(jsonData["InputDataList"]))
        self.setheader()
        self.wfile.write("<p>POST request received<p>".format(self.path).encode('utf-8'))


#Handler = serverResponseHandler()


#with socketserver.TCPServer(("", PORT), Handler) as httpd:
with socketserver.TCPServer(("", PORT), serverResponseHandler) as httpd:
    print("serving at port", PORT)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

    httpd.server_close()
    print("server stopped")
