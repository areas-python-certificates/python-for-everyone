# Dependencies.
import sqlite3

# SQLite connection.
connection = sqlite3.connect("assignment.sqlite")
cursor = connection.cursor()

# If the table exists, drop it. Then, create it.
cursor.execute("DROP TABLE IF EXISTS Counts")
cursor.execute("CREATE TABLE Counts (org TEXT, count INTEGER)")

# Get the file and open it.
filename = input("Enter file name: ")
if len(filename) == 0: filename = "mbox.txt"
filenameHandler = open(filename)

# Update the table with email counts.
for line in filenameHandler:
	if not line.startswith("From: "):
		continue
	words = line.split()
	email = words[1]
	domain = email.split("@")[1]
	
	cursor.execute("SELECT count FROM Counts WHERE org = ?", (domain,))
	match = cursor.fetchone()

	if match is None:
		cursor.execute("INSERT INTO Counts (org, count) VALUES (?, 1)", (domain,))
	else:
		cursor.execute("UPDATE Counts SET count = count + 1 WHERE org = ?", (domain,))

	connection.commit()

# Get the results.
sqlString = "SELECT org, count FROM Counts ORDER BY count DESC LIMIT 10"

for row in cursor.execute(sqlString):
	print(str(row[0]), row[1])

cursor.close()
