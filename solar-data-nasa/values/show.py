import sys, json
import SimpleHTTPServer
import SocketServer
import subprocess

nasa = open(sys.argv[1], 'r')
skipLine = 9
lineIndex = 0
result = []

for line in nasa:
	if lineIndex > skipLine:
		line = line.strip()
		v = line.split(' ')
		result.append([int(v[0]), int(v[1]), int(v[2]), int(float(v[6]))])

	lineIndex += 1
nasa.close()

res = open('result.json', 'w')
res.write(json.dumps(result))
res.close()

PORT = 8666

Handler = SimpleHTTPServer.SimpleHTTPRequestHandler

httpd = SocketServer.TCPServer(("", PORT), Handler)

print "serving at port", PORT
subprocess.call('sensible-browser "http://localhost:'+str(PORT)+'"', shell=True)
httpd.serve_forever()