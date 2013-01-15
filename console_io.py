# -*- coding: utf-8 -*-
# Copyright (c) 2012, Ivashin Alexey

import sys
import getopt

"""Additional gernerationg preference profiles methods for result printing."""

def simplify_print_profile(l):
	"""Just print a profile in numeric style
	For example this function prints
	3 0 0
	0 3 0
	0 0 3
	mean
	a a a
	b b b
	c c c
	"""
	m = len(l)
	for i in range(0, m):
		print(' '.join(map(lambda x: str(x), l[i])))
	print('===\n')

def convert_and_print_profile(l):
	"""Print a profile in humanable style
	For example this function prints
	a a a
	b b b
	c c c
	for profile matrix
	a a a
	b b b
	c c c
	"""
	m = len(l) #alternatives number 
	n = sum(l[0]) #experts number
	result = [[0 for j in range(n)] for i in range(m)]
	__convert_and_print_profile_recursive(l, 0, 0, [(z, False) for z in range(n)], result)
	for i in range(m):
		p = []
		for j in range(n):
			if result[i][j]>0:
				p.append(chr(96+result[i][j]))
			else:
				p.append(str(result[i][j]))
		print(' '.join(p))
	print('=======\n')

def __convert_and_print_profile_recursive(l, i, j, s, result):
	"""Recursive helper subdef for convert_and_print_profile function
	"""
	m = len(result) #alternatives number 
	n = len(result[0]) #experts number
	while(l[i][j] == 0):
		j = j + 1
		if (j >= m) :
			i = i + 1
			if (i>=m):
				return True
			j = 0
			s = [(z, False) for z in range(n)]
	cc = 0 #index of current candidate for the substitution
	for cc in range(len(s)):
		e = s[cc] #acting element
		k = e[0]
		if (result[j][k]==0) and (not e[1]):
			flag = True
			s[cc] = (k, True)
			result[j][k] = i + 1
			l[i][j] = l[i][j] - 1
			if __convert_and_print_profile_recursive(l, i, j, s, result):
				return True
			else:
				s[cc] = (k, False)
				result[j][k] = 0
				l[i][j] = l[i][j] + 1
	return False

def print_decomposition(l):
	"""Print a decomposition
	For example this function prints
	3 0 0   ( 3 )
	1+1+1
	1 1 0   ( 3 )
	1+2
	0 0 1   ( 3 )
	3
	"""
	n = len(l)
	for i in range(0, n):
		s = 0
		for j in range(0, len(l[i])):
			s = s + l[i][j]*(j+1)
		st = ''
		for j in range(0, len(l[i])):
			sst = '+'.join([str(j+1) for k in range(0, l[i][j])])
			if sst != '':
				if st=='':
					st = st + sst
				else:
					st = st + '+' + sst
		print(' '.join(map(lambda x: str(x), l[i])), '  (', s, ')')
		print(st)
	print('===\n')

def command_line_analys(argv):
	"""The analysis function of command-line arguments
	-n number of experts
	-m number of alternatives
	"""
	try:
		opts, args = getopt.getopt(argv, 'n:m:')
	except getopt.error:
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
		return (4, 4)

if __name__=='__main__':
	convert_and_print_profile([[1, 1, 1, 0], [1, 1, 0, 1], [1, 0, 0, 2],[0, 1, 2, 0]])
	convert_and_print_profile([[1, 1, 1, 0], [1, 0, 1, 1], [1, 2, 0, 0],[0, 0, 1, 2]])
	convert_and_print_profile([[1, 1, 1, 0], [0, 1, 1, 1], [2, 1, 0, 0],[0, 0, 1, 2]])
