import sys, json

grid = json.loads(open(sys.argv[1], 'r').read())
inter = grid['resources']

for i in inter:
	print i
	t = 0
	while t < len(inter[i]):
		tt = inter[i][t]
		qq = t+1
		if qq == len(inter[i]):
			qq = 0
		ntt = inter[i][qq]

		for tra in tt:
			for n in tra['to']:
				found = False
				for tra2 in ntt:
					if tra2['from'] == n['to']:
						found = True
						break

				if not found:
					print t, tra['from'], n['to'], 'not found'
		t += 1
	print