# -*- coding: utf-8 -*-
# Copyright (c) 2012, Ivashin Alexey
 
"""Core methods for gernerationg preference profiles."""

import sys
import math
import psycopg2
from itertools import combinations_with_replacement, permutations
from prints import simplify_print_profile, convert_and_print_profile, command_line_analys, print_decomposition

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
	return [[j for j in combs[i]] for i in c]

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
	try:
		conn = psycopg2.connect("host=db.fedul0x dbname=preferences_profile user=postgres password=postgres")
	except:
		print 'Can`t connect to database'
		return 1

	cur = conn.cursor()

	try: 
		cur.execute("CREATE TYPE profile_status AS ENUM ('uncheck', 'not_valid', 'ok')")
	except:
		print 'Relation profile_status already exists'
		conn.commit()

	try: 
		cur.execute("""
	CREATE TABLE combination_of_alternative_distribution (
	id serial PRIMARY KEY,
	dimension_n integer NOT NULL,
	dimension_m integer NOT NULL,
	combination integer[] NOT NULL, 
	UNIQUE (combination)
	);""")
	except:
		print 'Relation combination_of_alternative_distribution already exists'
		conn.commit()

	try: 
		cur.execute("""
	CREATE TABLE combination_of_combination_of_alternative_distribution (
	id serial PRIMARY KEY,
	dimension_n integer NOT NULL,
	dimension_m integer NOT NULL,
	combination_of_combination integer[] NOT NULL, 
	state profile_status,
	UNIQUE (combination_of_combination)
	);""")
	except:
		print 'Relation combination_of_combination_of_alternative_distribution already exists'
		conn.commit()
	conn.commit()





	cur.execute("""SELECT DISTINCT(combination) FROM combination_of_alternative_distribution 
	WHERE dimension_n = %s and dimension_m = %s""", (n, m))
	all_comb = [c[0] for c in cur.fetchall()]
	if len(all_comb)==0:
		all_comb = []
		for x in create_decomposition_into_components(n):
			# print_decomposition([x, x, x])
			l = interpretate_decomposition_to_sum_list(x, m)
			for p in permutations(l):
				if not (p in all_comb):
					all_comb.append(p)
					# print p
					try:
						cur.execute("""
					INSERT INTO combination_of_alternative_distribution (dimension_n, dimension_m, combination) 
					VALUES (%s, %s, %s)""", (n, m, [o for o in p]))
						print "Added %s" % (p, )
						conn.commit()
					except:
						print "Error %s" % (p, )
						pass
	

	cur.execute("""SELECT count(*) FROM combination_of_combination_of_alternative_distribution 
		WHERE dimension_n = %s and dimension_m = %s and state = %s""", (n, m, 'uncheck'))
	zz = cur.fetchone()[0]
	if (zz == 0):
		z = len(all_comb)
		k = 0
		for c in combinations_with_replacement([i for i in xrange(0, z)], m):
			try:
				cur.execute("""INSERT INTO combination_of_combination_of_alternative_distribution (dimension_n, dimension_m, combination_of_combination, state) 
				VALUES (%s, %s, %s, %s)""", (n, m, [o for o in c], 'uncheck'))
				conn.commit()
				print "Added %s" % (c, )
			except:
				print "Error %s" % (c, )
				pass

	currentLimit = 0
	currentOffset = 1
	stepLimit = 100
	currentLimit = currentLimit + stepLimit
	cur.execute("""SELECT id, combination_of_combination FROM combination_of_combination_of_alternative_distribution 
		WHERE dimension_n = %s and dimension_m = %s and state = %s ORDER BY id LIMIT %s """, (n, m, 'uncheck', currentLimit))
	all_comb_of_comb = cur.fetchall()
	zz = len(all_comb_of_comb)
	k = 0
	while (zz > 0):
		for c in all_comb_of_comb:
			# print c[1]
			if check_profile(make_profile(all_comb, c[1])):
				k = k + 1
				# simplify_print_profile(make_profile(all_comb, c))
				convert_and_print_profile(make_profile(all_comb, c[1]))
				cur.execute("""UPDATE combination_of_combination_of_alternative_distribution SET state = 'ok' WHERE id = %s; """, (c[0], ))
			else:
				cur.execute("""UPDATE combination_of_combination_of_alternative_distribution SET state = 'not_valid' WHERE id = %s; """, (c[0], ))
		conn.commit()	
		currentLimit = currentLimit + stepLimit
		currentOffset = currentOffset + stepLimit
		# cur.execute("""SELECT id, combination_of_combination FROM combination_of_combination_of_alternative_distribution 
			# WHERE dimension_n = %s and dimension_m = %s and state = %s  ORDER BY id LIMIT %s OFFSET %s""", (n, m, 'uncheck', currentLimit, currentOffset))
		cur.execute("""SELECT id, combination_of_combination FROM combination_of_combination_of_alternative_distribution 
			WHERE dimension_n = %s and dimension_m = %s and state = %s  ORDER BY id LIMIT %s""", (n, m, 'uncheck', currentLimit))
		all_comb_of_comb = cur.fetchall()
		zz = len(all_comb_of_comb)
		print "%s - %s" % (currentOffset, currentLimit)

	print k
	conn.commit()

	cur.close()
	conn.close()



if __name__ == '__main__':
	global EXPERTS_NUM
	global ALTERNATIVS_NUM

	EXPERTS_NUM, ALTERNATIVS_NUM = command_line_analys(sys.argv[1:])

	main()
