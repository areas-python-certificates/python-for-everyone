# Dependencies.
import sqlite3

# Connect to the database.
connect = sqlite3.connect("spider.sqlite")
cursor = connect.cursor()

# Select the data.
cursor.execute(
	'''
		SELECT
			COUNT(from_id) AS inbound,
			old_rank,
			new_rank,
			id,
			url 
		FROM
			Pages p
		JOIN
			Links l
		ON p.id = l.to_id
		WHERE
			html IS NOT NULL
		GROUP BY
			id
		ORDER BY
			inbound DESC
	'''
)

# Print the data.
count = 0
for row in cursor:
	if count < 50: print(row)
	count = count + 1

print(count, "rows.")

cursor.close()
