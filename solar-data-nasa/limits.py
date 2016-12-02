res = open('limits.txt', 'w')
summ = 0

for i in range(20):
	ff = open('i%d.txt' % (i,), 'r')
	skipLine = 9
	lineIndex = 0

	maxv = 0
	minv = 1000

	for line in ff:
		if lineIndex > skipLine:
			line = line.strip()
			v = line.split(' ')
			vv = int(float(v[6]))

			if vv > maxv:
				maxv = vv

			if vv < minv:
				minv = vv

		lineIndex += 1

	ff.close()
	print 'i%d:\t\tmin: %d\t\tmax: %d' % (i, minv, maxv)
	res.write('i%d:\t\tmin: %d\t\tmax: %d\n' % (i, minv, maxv))
	summ += maxv

print '\t\t\t\t\tsum: %d' % (summ,)
res.write('\t\t\t\t\tsum: %d\n' % (summ,))
res.close()