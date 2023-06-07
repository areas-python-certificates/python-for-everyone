# Dependencies.
import json
import sqlite3

# Get the file.
filename = input("Enter the filename: ")
if len(filename) == 0: filename = "roster.json"

# Parse the JSON.
jsonFile = open(filename).read()
jsonArrayOfArrays = json.loads(jsonFile)

# Connect to the database.
connect = sqlite3.connect("roster.sqlite")
cursor = connect.cursor()

# Create the tables (if they already exist, drop them beforehand).
cursor.executescript(
  '''
		DROP TABLE IF EXISTS User;
		DROP TABLE IF EXISTS Member;
		DROP TABLE IF EXISTS Course;

		CREATE TABLE User (
			id		INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
			name	TEXT UNIQUE
		);

		CREATE TABLE Course (
			id		INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
			title	TEXT UNIQUE
		);

		CREATE TABLE Member (
			user_id			INTEGER,
			course_id		INTEGER,
			role				INTEGER,
			PRIMARY KEY	(user_id, course_id)
		);
  '''
)

# Insert the data.
for jsonArray in jsonArrayOfArrays:
	# Prepare the data.
	userName = jsonArray[0]
	courseTitle = jsonArray[1]
	memberRole = jsonArray[2]

	# Insert the user.
	cursor.execute('''
		INSERT OR IGNORE INTO User (name)
		VALUES ( ? )''', ( userName, )
	)
	cursor.execute( 'SELECT id FROM User WHERE name = ? ', ( userName, ) )
	userId = cursor.fetchone()[0]

	# Insert the course.
	cursor.execute('''
		INSERT OR IGNORE INTO Course (title)
		VALUES ( ? )''', ( courseTitle, ) )
	cursor.execute( 'SELECT id FROM Course WHERE title = ? ', ( courseTitle, ) )
	courseId = cursor.fetchone()[0]

	# Insert the member.
	cursor.execute('''
		INSERT OR REPLACE INTO Member
		( user_id, course_id, role ) VALUES ( ?, ?, ? )''', ( userId, courseId, memberRole )
	)

	connect.commit()
