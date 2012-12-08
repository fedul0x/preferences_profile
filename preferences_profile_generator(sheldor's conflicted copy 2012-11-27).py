# -*- coding: utf-8 -*-
import math
from xpermutations import *
from itertools import combinations_with_replacement

def print_profile_from_decomposition(a):
	return 0

def simplify_print_list(l):
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

def create_decomposition_into_components(k):
	if k <= 0:
		return []
	l = [[0 for i in xrange(0, k)]] #list of lists that contains result
	l[0][0] = k
	cis = [1] #list of ci-values for begin of decomposition in current set
	cs = 0 #cs - current set of components for decomposition
	while (cs < len(cis)):
		#ci - index of component for set value
		for ci in xrange(cis[cs]+1, k+1):
			mi = 1 # index of component for get value
			m = l[cs][mi-1] #value of mi
			n = m*mi/ci#numbers of posible decompositions
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
	return [combs[i] for i in c]


def check_profile(a):
	n = EXPERTS_NUM
	m = ALTERNATIVS_NUM
	# simplify_print_list(a)
	for i in xrange(0, m):
		s = 0
		for j in xrange(0, m):
			s = s + a[j][i]
		if s != n:
			return False
	return True

def main():
	n = EXPERTS_NUM # кол-во экспертов 
	m = ALTERNATIVS_NUM # кол-во альтернатив

	print_decomposition (create_decomposition_into_components(10))
	return
	# for c in xselections([i for i in xrange(0, 2)], 2):
	# 	print c
	# return 

	all_comb = []
	for x in create_decomposition_into_components(n):
		l = interpretate_decomposition_to_sum_list(x, m)
		for p in xpermutations(l):
			if not (p in all_comb):
				all_comb.append(p)
	# print(all_comb)

	z = len(all_comb)
	k = 0
	# for c in xselections([i for i in xrange(0, z)], m): #ERROR
	for c in combinations_with_replacement([i for i in xrange(0, z)], m): #ERROR
		if check_profile(make_profile(all_comb, c)):
			print c
			k = k + 1
			simplify_print_list(make_profile(all_comb, c))
	print k


if __name__ == '__main__':
	global EXPERTS_NUM
	global ALTERNATIVS_NUM

	ALTERNATIVS_NUM = 5
	EXPERTS_NUM = 6

	main()

#	l = interpretate_decomposition_to_sum_list(create_decomposition_into_components(3)[0])
#	for uc in xcombinations(l,3): 
#		print ''.join(str(uc))
	# print xuniqueCombinations(interpretate_decomposition_to_sum_list(create_decomposition_into_components(3)[0]), 3)
