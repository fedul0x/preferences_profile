# -*- coding: utf-8 -*-
# Copyright (c) 2012, Ivashin Alexey

import sys
import getopt

"""Additional gernerationg preference profiles methods for result printing."""

def simplify_print_profile(l):
	m = len(l)
	for i in xrange(0, m):
		print ' '.join(map(lambda x: str(x), l[i]))
	print '===\n'

def convert_and_print_profile(l): #l - mxm matrix
	m = len(l) #alternatives number 
	n = sum(l[0]) #experts number
	result = [[0 for j in xrange(n)] for i in xrange(m)]
	convert_and_print_profile_recursive(l, 0, 0, [z for z in xrange(n)], result)
	for i in xrange(m):
		p = []
		for j in xrange(n):
			if result[i][j]>0:
				p.append(chr(96+result[i][j]))
			else:
				p.append(str(result[i][j]))
		print ' '.join(p)
	print '=======\n'

def convert_and_print_profile_recursive(l, i, j, s, result): #l - mxm matrix
	m = len(result) #alternatives number 
	n = len(result[0]) #experts number
	k = 0
	if (l[i][j] > 0):
		if (s == []):
			return False
		else:
			k = s[0]
			s = s[1:]
			cc = 0
			while result[j][k]!=0:
				s.append(k)
				k = s[0]
				s = s[1:]
				cc = cc + 1
				if cc >len(s):
					return False
			result[j][k] = i + 1
			l[i][j] = l[i][j] - 1
	else:
		j = j + 1
		if (j<m):
			pass
		else:
			i = i + 1
			j = 0
			s = [z for z in xrange(n)]
	if (i >= m):
		return True
	else:
		if convert_and_print_profile_recursive(l, i, j, s, result):
			return True
		else:
			return False

def print_decomposition(l):
	n = len(l)
	for i in xrange(0, n):
		s = 0
		for j in xrange(0, len(l[i])):
			s = s + l[i][j]*(j+1)
		st = ''
		for j in xrange(0, len(l[i])):
			sst = '+'.join([str(j+1) for k in xrange(0, l[i][j])])
			if sst != '':
				if st=='':
					st = st + sst
				else:
					st = st + '+' + sst
		print ' '.join(map(lambda x: str(x), l[i])), '  (', s, ')'
		print st
	print '===\n'

def command_line_analys(argv):
	try:
		opts, args = getopt.getopt(argv, 'n:m:')
	except getopt.error, msg:
		return (3, 3)
    # process options
	n = -1
	m = 0
	for o, a in opts:
		if o == '-n':
			n = int(a)
		if o == '-m':
			m = int(a)
	if n*m > 0:
		return (n, m)
	else:
		return (3, 4)

def print_profile_from_decomposition(a):
	return 0


if __name__=='__main__':
	# convert_and_print_profile([[3, 0, 0], [0, 1, 2], [0, 2, 1]])
	# convert_and_print_profile([[3, 0, 0], [0, 3, 0], [0, 0, 3]])
	# convert_and_print_profile([[2, 2], [2, 2]])
	# convert_and_print_profile([[4, 0], [0, 4]])
	# convert_and_print_profile([[3, 1], [1, 3]])
	print '4x3'
	convert_and_print_profile([[1, 1, 2], [1, 1, 2], [2, 2, 0]])
	print 'end'
