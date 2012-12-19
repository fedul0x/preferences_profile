# -*- coding: utf-8 -*-
# Copyright (c) 2012, Ivashin Alexey

import sys
import getopt

"""Additional gernerationg preference profiles methods for result printing."""

def simplify_print_profile(l):
	n = len(l)
	for i in xrange(0, n):
		print ' '.join(map(lambda x: str(x), l[i]))
	print '===\n'

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
		return (3, 3)

def print_profile_from_decomposition(a):
	return 0