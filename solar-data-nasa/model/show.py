import sys, json
import SimpleHTTPServer
import SocketServer
import subprocess

nasa = open(sys.argv[1], 'r')
skipLine = 9
lineIndex = 0
result = {}
p = [0, 0, 0, 0]

for line in nasa:
	if lineIndex > skipLine:
		line = line.strip()
		v = line.split(' ')
		r = [int(v[0]), int(v[1]), int(v[2]), int(float(v[6]))]

		if p[1] not in result:
			result[p[1]] = {}

		if p[2] not in result[p[1]]:
			result[p[1]][p[2]] = {}

		if p[3] not in result[p[1]][p[2]]:
			result[p[1]][p[2]][p[3]] = {}

		if r[3] not in result[p[1]][p[2]][p[3]]:
			result[p[1]][p[2]][p[3]][r[3]] = 0

		result[p[1]][p[2]][p[3]][r[3]] += 1

		p = r

	lineIndex += 1
nasa.close()

prob = {}
for m in result:
	prob[m] = {}
	for d in result[m]:
		prob[m][d] = {}
		for s in result[m][d]:
			b = 0
			prob[m][d][s] = {}
			for ns in result[m][d][s]:
				prob[m][d][s][ns] = result[m][d][s][ns]
				b += result[m][d][s][ns]

			b = float(b)

			for ns in result[m][d][s]:
				prob[m][d][s][ns] = prob[m][d][s][ns] / b

nodes = []
edges = []

interGroupGap = 150
intraGroupGap = 300
graphGap = 100

m = int(sys.argv[2])
for d in prob[m]:
	y = 0
	for s in prob[m][d]:
		nodes.append({'id': '%d-%d' % (d, s), 'label': s, 'group': d, 'x': d*intraGroupGap, 'y': y*interGroupGap})

		for ns in prob[m][d][s]:
			edges.append({'from': '%d-%d' % (d, s), 'to': '%d-%d' % (d+1, ns), 'label': '%.2f' % (prob[m][d][s][ns],), 'arrows': 'to'})

		y += 1


res = open('result.json', 'w')
res.write(json.dumps({'nodes': nodes, 'edges': edges}))
res.close()

PORT = 8666

Handler = SimpleHTTPServer.SimpleHTTPRequestHandler

httpd = SocketServer.TCPServer(("", PORT), Handler)

print "serving at port", PORT
subprocess.call('sensible-browser "http://localhost:'+str(PORT)+'"', shell=True)
httpd.serve_forever()"""