import os
import glob
import sqlite3 as sql

database = 'src/database/ojms.db'
connection = None

def sql_init():
	if not os.path.isfile(database):
		global connection
		create_tables()
		create_oj_database()
		connection.close()
		connection = None

def sql_connect():
	global connection
	if connection == None:
		connection = sql.connect(database)
		connection.isolation_level = None
	return connection

def create_tables():
	connection = sql_connect()
	cursor = connection.cursor()
	path = 'src/schema'
	for sqlfilename in glob.glob(os.path.join(path, '*.sql')):
		sqlFile = open(sqlfilename, 'r')
		sqlScript = sqlFile.read()
		sqlFile.close()
		cursor.executescript(sqlScript)
	connection.commit()
	print "Executed table schema."


def create_oj_database():
	connection = sql_connect()
	cursor = connection.cursor()
	path = 'src/database'
	for inputfilename in glob.glob(os.path.join(path, '*.sql')):
		inputFile=open(inputfilename,'r')
		Query=inputFile.readline().rstrip("\n")
		for line in inputFile:
			line=line.rstrip(",;\n")
			insertQuery=Query+line+";"
			cursor.execute(insertQuery)
		connection.commit()
		print "Inserted values into",inputfilename[13:-4]
	print "Database created"

def username_exists(username):
	if username is "" :
		return True
	connection = sql_connect()
	cursor = connection.cursor()
	cursor.execute('SELECT * FROM user WHERE username=?', username)
	return cursor.fetchone() is not None

def email_exists(email):
	if email is "" :
		return True
	connection = sql_connect()
	cursor = connection.cursor()
	cursor.execute('SELECT * FROM user WHERE email=?', email)
	return cursor.fetchone() is not None

def add(fname,lname,email,username,password,country,dob,oname,otype,ocity,ocountry):
	connection = sql_connect()
	cursor = connection.cursor()
    	cursor.execute("INSERT INTO user (username,password,fname,lname,country,dob) VALUES (?,?,?,?,?.?)", (username,password,fname,lname,country,dob))
	cursor.execute("INSERT INTO organisation (oname, otype, ocity, ocountry) VALUES (?,?,?,?)", (oname,otype,ocity,ocountry))
	connection.commit()
	print "user added"


def get_user(email, password):
	connection = sql_connect()
	cursor = connection.cursor()
	t = (email, password,)
	cursor.execute('SELECT * FROM user WHERE email=? AND password=?', t)
	row = cursor.fetchone()
	if row is None:
		raise ValueError("Invalid Credentials")
	return row