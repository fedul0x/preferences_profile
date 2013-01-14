# -*- coding: utf-8 -*-
# Copyright (c) 2012, Ivashin Alexey
 
"""Core methods for gernerationg preference profiles."""

import sys
import math
import psycopg2
from database  import create_connection_and_tables
from itertools import combinations_with_replacement, permutations
from prints    import simplify_print_profile, convert_and_print_profile, command_line_analys, print_decomposition

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

	(connection, cursor) = create_connection_and_tables()

	# k = 0
	# for x in create_decomposition_into_components(n):
	# 	l = interpretate_decomposition_to_sum_list(x, m)
	# 	for p in permutations(l):
	# 		k = k + 1
	# print k
	# return None

	cursor.execute("SELECT id, state FROM profiles_type WHERE dimension_n = %s and dimension_m = %s", (n, m))
	res = cursor.fetchone()
	print res
	if cursor.rowcount != 1:
		if cursor.rowcount > 1:
			cursor.execute("DELETE FROM profiles_type WHERE dimension_n = %s and dimension_m = %s",	(n, m))
			connection.commit()
		print 'insert processing'
		cursor.execute("""INSERT INTO profiles_type (dimension_n, dimension_m, state)
			VALUES (%s, %s, %s)""", (n, m, 'processing'))
		cursor.execute("SELECT id, state FROM profiles_type WHERE dimension_n = %s and dimension_m = %s", (n, m))
		res = cursor.fetchone()
		connection.commit()
		all_comb = []
		for x in create_decomposition_into_components(n):
			l = interpretate_decomposition_to_sum_list(x, m)
			for p in permutations(l):
				if not (p in all_comb):
					all_comb.append(p)
					try:
					# print res[0], [o for o in p]
						cursor.execute("""
							INSERT INTO combination_of_alternative_distribution (profiles_type_id, combination) 
							VALUES (%s, %s)""", (res[0], [o for o in p]))
						print "Added %s" % (p, )
						connection.commit()
					except:
						print "Error %s" % (p, )
						connection.commit()
		cursor.execute("SELECT id, state FROM profiles_type WHERE dimension_n = %s and dimension_m = %s", (n, m))
		res = cursor.fetchone()
		cursor.execute("""UPDATE profiles_type SET state = 'filling' WHERE id = %s; """, (res[0], ))
		connection.commit()

	cursor.execute("SELECT id, state FROM profiles_type WHERE dimension_n = %s and dimension_m = %s", (n, m))
	res = cursor.fetchone()
	print res
	if cursor.rowcount == 1:
		if res[1] == 'processing':
			all_comb = []
			for x in create_decomposition_into_components(n):
				l = interpretate_decomposition_to_sum_list(x, m)
				for p in permutations(l):
					if not (p in all_comb):
						all_comb.append(p)
						try:
							cursor.execute("""
								INSERT INTO combination_of_alternative_distribution (profiles_type_id, combination) 
								VALUES (%s, %s)""", (res[0], [o for o in p]))
							print "Added %s" % (p, )
							connection.commit()
						except:
							print "Error %s" % (p, )
							connection.commit()
			cursor.execute("""UPDATE profiles_type SET state = 'filling' WHERE id = %s; """, (res[0], ))
			connection.commit()
		cursor.execute("SELECT id, state FROM profiles_type WHERE dimension_n = %s and dimension_m = %s", (n, m))
		res = cursor.fetchone()
		print res
		if res[1] == 'filling':
			cursor.execute("""SELECT DISTINCT(combination) FROM combination_of_alternative_distribution 
				WHERE profiles_type_id = %s""", (res[0],))
			all_comb = [c[0] for c in cursor.fetchall()]
			z = len(all_comb)
			k = 0
			for c in combinations_with_replacement([i for i in xrange(0, z)], m):
				try:
					cursor.execute("""INSERT INTO combination_of_combination_of_alternative_distribution (profiles_type_id, combination_of_combination, state) 
						VALUES (%s, %s, %s)""", (res[0], [o for o in c], 'uncheck'))
					connection.commit()
					print "Added %s" % (c, )
				except:
					print "Error %s" % (c, )
					connection.commit()
			cursor.execute("""UPDATE profiles_type SET state = 'checking' WHERE id = %s; """, (res[0], ))
			connection.commit()
			cursor.execute("""SELECT DISTINCT(combination) FROM combination_of_alternative_distribution 
				WHERE profiles_type_id = %s""", (res[0],))
			all_comb = [c[0] for c in cursor.fetchall()]

		cursor.execute("SELECT id, state FROM profiles_type WHERE dimension_n = %s and dimension_m = %s", (n, m))
		res = cursor.fetchone()
		print res
		if res[1] == 'checking':
			cursor.execute("""SELECT DISTINCT(combination) FROM combination_of_alternative_distribution 
				WHERE profiles_type_id = %s""", (res[0],))
			all_comb = [c[0] for c in cursor.fetchall()]
		
		cursor.execute("SELECT id, state FROM profiles_type WHERE dimension_n = %s and dimension_m = %s", (n, m))
		res = cursor.fetchone()
		print res
		if res[1] == 'ok':
			print 'This task is ok!'
			cursor.close()
			connection.close()
			return 0
	# 	else:
	# 		print 'Unknown status %s' % (res[1], )
	# 		return 0
	# else:


	# currentLimit = 0
	# currentOffset = 1
	stepLimit = 100
	# currentLimit = currentLimit + stepLimit
	# TODO add change status to process
	cursor.execute("""SELECT id, combination_of_combination FROM combination_of_combination_of_alternative_distribution 
		WHERE profiles_type_id = %s and state = %s ORDER BY id LIMIT %s """, (res[0], 'uncheck', stepLimit))
	all_comb_of_comb = cursor.fetchall()
	zz = len(all_comb_of_comb)
	k = 0
	while (zz > 0):
		for c in all_comb_of_comb:
			if check_profile(make_profile(all_comb, c[1])):
				k = k + 1
				# simplify_print_profile(make_profile(all_comb, c))
				convert_and_print_profile(make_profile(all_comb, c[1]))
				cursor.execute("""UPDATE combination_of_combination_of_alternative_distribution SET state = 'ok' WHERE id = %s; """, (c[0], ))
			else:
				cursor.execute("""UPDATE combination_of_combination_of_alternative_distribution SET state = 'not_valid' WHERE id = %s; """, (c[0], ))
			connection.commit()	
		# currentLimit = currentLimit + stepLimit
		# currentOffset = currentOffset + stepLimit
		# cur.execute("""SELECT id, combination_of_combination FROM combination_of_combination_of_alternative_distribution 
			# WHERE dimension_n = %s and dimension_m = %s and state = %s  ORDER BY id LIMIT %s OFFSET %s""", (n, m, 'uncheck', currentLimit, currentOffset))
		cursor.execute("""SELECT id, combination_of_combination FROM combination_of_combination_of_alternative_distribution 
			WHERE profiles_type_id = %s and state = %s  ORDER BY id LIMIT %s""", (res[0], 'uncheck', stepLimit))
		all_comb_of_comb = cursor.fetchall()
		zz = len(all_comb_of_comb)
		# print "%s - %s" % (currentOffset, currentLimit)
	cursor.execute("""UPDATE profiles_type SET state = 'ok' WHERE id = %s; """, (res[0], ))
	print k
	connection.commit()
	print 'This task is ok!'
	cursor.close()
	connection.close()


if __name__ == '__main__':
	global EXPERTS_NUM
	global ALTERNATIVS_NUM

	EXPERTS_NUM, ALTERNATIVS_NUM = command_line_analys(sys.argv[1:])

	main()
