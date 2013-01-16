# -*- coding: utf-8 -*-
# Copyright (c) 2013, Ivashin Alexey

from psycopg2 import *

"""Methods for database connecting and create all necessary tables."""

def create_connection_and_tables():
	"""Make and return connection to database and cursor.
	Create types:
	* profile_status
	* profile_type_status
	Create relations:
	* profiles_type
	* combination_of_alternative_distribution
	* combination_of_combination_of_alternative_distribution"""
	try:
		conn = connect("host=db.fedul0x dbname=preferences_profile user=postgres password=postgres")
	except OperationalError as e:
		# print(e.message)
		raise
	cur = conn.cursor()
	try: 
		cur.execute("CREATE TYPE profile_status AS ENUM ('uncheck', 'process', 'not_valid', 'ok')")
	except ProgrammingError as e:
		# print(e.message)
		pass
	except:
		# print(e.message)
		raise
	conn.commit()
	try: 
		cur.execute("CREATE TYPE profile_type_status AS ENUM ('processing', 'filling', 'checking', 'ok')")
	except ProgrammingError as e:
		# print(e.message)
		pass
	except:
		# print(e.message)
		raise
	conn.commit()
	try: 
		cur.execute("""
	CREATE TABLE profiles_type (
	id serial PRIMARY KEY,
	dimension_n integer NOT NULL,
	dimension_m integer NOT NULL,
	state profile_type_status
	);""")
	except ProgrammingError as e:
		# print(e.message)
		pass
	except:
		# print(e.message)
		raise
	conn.commit()

	try: 
		cur.execute("""
	CREATE TABLE combination_of_alternative_distribution (
	id serial PRIMARY KEY,
	profiles_type_id integer REFERENCES profiles_type,
	combination integer[] NOT NULL, 
	UNIQUE (profiles_type_id, combination)
	);""")
	except ProgrammingError as e:
		pass
		# print(e.message)
	except:
		# print(e.message)
		raise
	conn.commit()
	try: 
		cur.execute("""
	CREATE TABLE combination_of_combination_of_alternative_distribution (
	id serial PRIMARY KEY,
	profiles_type_id integer REFERENCES profiles_type,
	combination_of_combination integer[] NOT NULL, 
	state profile_status,
	UNIQUE (profiles_type_id, combination_of_combination)
	);""")
	except ProgrammingError as e:
		# print(e.message)
		pass
	except:
		# print(e.message)
		raise
	conn.commit()
	return (conn, cur)

if __name__ == '__main__':
	create_connection_and_tables()