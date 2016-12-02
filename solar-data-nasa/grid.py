import sys, json

props = json.loads(open('prop.json', 'r').read())
grid = json.loads(open('solar-grid-raw.json', 'r').read())

m = int(sys.argv[1])
minDay = 100

grid['resources'] = {}
grid['generators'] = {}
grid['loads'] = {}


for i in range(20):
	nasa = open('i%d.txt' % i, 'r')
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

	r = 'i%d' % i
	grid['resources'][r] = []

	for d in prob[m]:
		states = []
		for s in prob[m][d]:
			state = {'from': s, 'to': []}

			for ns in prob[m][d][s]:
				state["to"].append({"to": ns, "prob": prob[m][d][s][ns]})

			states.append(state)

		grid['resources'][r].append(states)

	if len(prob[m]) < minDay:
		minDay = len(prob[m])




for i in range(20):
	v = 'v%d' % i
	g = 'g%d' % i
	l = 'l%d' % i
	r = 'i%d' % i

	grid['nodes'][v]['generators'] = [g]
	grid['nodes'][v]['resources'] = [r]
	grid['nodes'][v]['loads'] = [l]

	grid['generators'][g] = props['generators'][g]
	grid['loads'][l] = props['loads'][l] * -1

grid['options']['number-of-time-steps'] = minDay

sg = open('solar-grid.json', 'w')
sg.write(json.dumps(grid))
sg.close()