# -*- coding: utf-8 -*-
# Copyright (c) 2012, Ivashin Alexey
 

"""Core methods for gernerationg preference profiles."""

import sys
import math
from itertools import combinations_with_replacement, permutations
from prints import simplify_print_profile, command_line_analys

def create_decomposition_into_components(k):
	"""Create a decomposition into component for k value,
	that components in a sum must set k value, for example
	k = 3
	return [[3, 0, 0], [1, 1, 0], [0, 0, 1]]
	that mean 1+1+1, 1+2, 3"""
	if k <= 0:
		return []
	l = [[0 for i in xrange(0, k)]] #list of lists that contatin result
	l[0][0] = k
	cis = [1] #list of ci-values for begin of decomposition in current set
	cs = 0 #current set of components for decomposition
	while (cs < len(cis)):
		#ci - index of component for set value
		for ci in xrange(cis[cs]+1, k+1):
			mi = 1 # index of component for get value
			m = l[cs][mi-1] #value of mi
			n = m*mi/ci #numbers of posible decompositions
			if n>=1:
				for c in xrange(1, math.trunc(n)+1):
					if (m*mi - c*ci)%mi == 0:
						l.append(l[cs][:])
						#change adding item
						l[len(l)-1][mi-1] = (m*mi - c*ci)/mi
						l[len(l)-1][ci-1] = c
						cis.append(ci)
		cs = cs + 1
	return l

def interpretate_decomposition_to_sum_list(l, e = 0):
	"""Reinterpretate a decomposition into list of values, sum of that
	equvivalent of k value, for example
	l = [3, 0, 0]
	return [1, 1, 1] mean 1+1+1
	l = [1, 1, 0]
	return [1, 2, 0] mean 1+2
	l = [0, 0, 1]
	return [3, 0, 0] mean 3"""
	result = []
	for j in xrange(0, len(l)):
		result.extend([(j+1) for k in xrange(0, l[j])])
	s = 0
	for j in xrange(0, len(l)):
		s = s + l[j]*(j+1)
	if e == 0:
		result.extend([0 for j in xrange(0, s-len(result))])
	else:
		result.extend([0 for j in xrange(0, e-len(result))])
	return result

def make_profile(combs, c):
	"""Return a profile, that generated from 
	from combinations list combs with indexes from c"""
	return [combs[i] for i in c]

def check_profile(a):
	"""Check generated profile for sum function
	Sum by columns must equal to experts number value"""
	n = EXPERTS_NUM
	m = ALTERNATIVS_NUM
	for i in xrange(0, m):
		s = 0
		for j in xrange(0, m):
			s = s + a[j][i]
		if s != n:
			return False
	return True

def main():
	n = EXPERTS_NUM
	m = ALTERNATIVS_NUM

	all_comb = []
	for x in create_decomposition_into_components(n):
		l = interpretate_decomposition_to_sum_list(x, m)
		for p in permutations(l):
			if not (p in all_comb):
				all_comb.append(p)

	z = len(all_comb)
	k = 0
	for c in combinations_with_replacement([i for i in xrange(0, z)], m):
		if check_profile(make_profile(all_comb, c)):
			print c
			k = k + 1
			simplify_print_profile(make_profile(all_comb, c))
	print k



if __name__ == '__main__':
	global EXPERTS_NUM
	global ALTERNATIVS_NUM

	EXPERTS_NUM, ALTERNATIVS_NUM = command_line_analys(sys.argv[1:])

	main()
