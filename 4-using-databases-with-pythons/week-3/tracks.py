# Dependencies.
import xml.etree.ElementTree as et
import sqlite3

# Get the file.
filename = input("Enter the filename: ")
if len(filename) == 0: filename = "Library.xml"

# Parse the XML.
xml = et.parse(filename)
xmlTracks = xml.findall("dict/dict/dict")

# Create a list of dictionaries.
tracks = list()
for xmlTrack in xmlTracks:
	track = dict()
	for key, value in zip( list(xmlTrack)[::2], list(xmlTrack)[1::2] ):
		track[key.text] = value.text
	tracks.append(track)

# Connect to the database.
connect = sqlite3.connect("tracks.sqlite")
cursor = connect.cursor()

# Create the tables (if they already exist, drop them beforehand).
cursor.executescript(
	'''
		DROP TABLE IF EXISTS Genre;
		DROP TABLE IF EXISTS Artist;
		DROP TABLE IF EXISTS Album;
		DROP TABLE IF EXISTS Track;

		CREATE TABLE Genre (
			id		INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
			name	TEXT UNIQUE
		);

		CREATE TABLE Artist (
			id		INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
			name	TEXT UNIQUE
		);

		CREATE TABLE Album (
			id				INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
			artist_id	INTEGER,
			title			TEXT UNIQUE
		);

		CREATE TABLE Track (
			id				INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
			title			TEXT  UNIQUE,
			album_id	INTEGER,
			genre_id	INTEGER
		);
	'''
)

# Insert the data.
for track in tracks:
	# Skip tracks with missing data.
	if "Track ID" not in track or track["Track ID"] is None: continue
	if "Name" not in track or track["Name"] is None: continue
	if "Album" not in track or track["Album"] is None: continue
	if "Artist" not in track or track["Artist"] is None: continue
	if "Genre" not in track or track["Genre"] is None: continue

	# Get the data.
	trackName = track["Name"]
	trackAlbum = track["Album"]
	trackArtist = track["Artist"]
	trackGenre = track["Genre"]

	# Insert the genre.
	cursor.execute(
		'''INSERT OR IGNORE INTO Genre (name)
		   VALUES ( ? )''',( trackGenre,)
	)
	cursor.execute( 'SELECT id FROM Genre WHERE name = ? ', ( trackGenre, ) )
	genreId = cursor.fetchone()[0]

	# Insert the artist.
	cursor.execute('''
		INSERT OR IGNORE INTO Artist (name)
		VALUES ( ? )''', ( trackArtist, )
	)
	cursor.execute( 'SELECT id FROM Artist WHERE name = ? ', ( trackArtist, ) )
	artistId = cursor.fetchone()[0]

	# Insert the album.
	cursor.execute('''
		INSERT OR IGNORE INTO Album (title, artist_id)
		VALUES ( ?, ? )''', ( trackAlbum, artistId )
	)
	cursor.execute( 'SELECT id FROM Album WHERE title = ? ', (trackAlbum,) )
	albumId = cursor.fetchone()[0]

	# Insert the track.
	cursor.execute('''
		INSERT OR REPLACE INTO Track ( title, album_id, genre_id )
		VALUES ( ?, ?, ? )''', ( trackName, albumId, genreId )
	)

	connect.commit()
