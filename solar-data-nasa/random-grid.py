import json, random

gens = [10, 13, 14, 15, 20, 20, 22, 22, 24, 24, 24, 24, 25, 25, 25, 25]
co = [0.2, 0.3, 0.35, 0.4, 0.5, 0.7]
loads = [16, 18, 18, 19, 19, 19, 21, 21, 28, 28]


data = {'generators': {}, 'loads': {}}
for i in range(20):
	g = {"CO": random.choice(co), "maxValue": random.choice(gens)}
	data['generators']['g%d' % i] = g
	data['loads']['l%d' % i] = random.choice(loads)
	

res = open('prop.json', 'w')
res.write(json.dumps(data, indent=4))
res.close()