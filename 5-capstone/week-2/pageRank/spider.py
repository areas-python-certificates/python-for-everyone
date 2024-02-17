# Dependencies.
import sqlite3
import ssl
from urllib.parse import urljoin
from urllib.parse import urlparse
from urllib.request import urlopen
import urllib.error # delete or add error handling.
from bs4 import BeautifulSoup

# Connect to the database.
connection = sqlite3.connect('spider.sqlite')
cursor = connection.cursor()

# Create tables (if they don't exist).
cursor.executescript(
	'''
		CREATE TABLE IF NOT EXISTS Pages (
			id INTEGER PRIMARY KEY,
			url TEXT UNIQUE,
			html TEXT,
			error INTEGER,
			old_rank REAL,
			new_rank REAL
		);

		CREATE TABLE IF NOT EXISTS Links (
			from_id INTEGER,
			to_id INTEGER,
			UNIQUE(from_id, to_id)
		);
		
		CREATE TABLE IF NOT EXISTS Webs (
			url TEXT UNIQUE
		);
	'''
)

# Search the database for a page to crawl.
cursor.execute(
	'''
		SELECT id, url
		FROM Pages
		WHERE html IS NULL AND error IS NULL
		ORDER BY RANDOM()
		LIMIT 1
	'''
)

pageToCrawl = cursor.fetchone()

# If there’s a page to crawl, let the user know.
if pageToCrawl is not None:
	print("Continuing to crawl. (To start over, delete spider.sqlite.)")

# Else, start a new crawl.
else:
	newPageToCrawl = input("Enter a new page to crawl (URL): ")
	if len(newPageToCrawl) == 0: newPageToCrawl = "http://python-data.dr-chuck.net/"
	
	if newPageToCrawl.endswith("/"): newPageToCrawl = newPageToCrawl[:-1]
	
	url = newPageToCrawl
	
	if newPageToCrawl.endswith(".htm") or newPageToCrawl.endswith(".html"):
		position = newPageToCrawl.rfind("/")
		url = newPageToCrawl[:position]

	if len(url) > 1:
		cursor.execute('''
			INSERT OR IGNORE INTO Webs (url)
			VALUES ( ? )''', ( url, )
		)
		cursor.execute('''
			INSERT OR IGNORE INTO Pages (url, html, new_rank)
			VALUES ( ?, NULL, 1.0 )''', ( newPageToCrawl, )
		)
		
		connection.commit()

# Get the URLs.
cursor.execute(
	'''
		SELECT url
		FROM Webs
	'''
)

pagesToCrawl = cursor

urls = list()
for pageToCrawl in pagesToCrawl:
	urls.append( str(pageToCrawl[0]) )

print(urls)

# SSL workaround.
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Get the pages.
pagesLeftToCrawl = 0

while True:
	if pagesLeftToCrawl < 1:
		totalPagesToCrawl = input("Enter the number of pages you want to crawl: ")
		if len(totalPagesToCrawl) < 1: break
		pagesLeftToCrawl = int(totalPagesToCrawl)

	pagesLeftToCrawl -= 1

	cursor.execute(
		'''
			SELECT id, url
			FROM Pages
			WHERE html IS NULL AND error IS NULL
			ORDER BY RANDOM()
			LIMIT 1
		'''
	)

	try:
		pageToCrawl = cursor.fetchone()
		fromId = pageToCrawl[0]
		newPageToCrawl = pageToCrawl[1]
	except:
		print("All pages crawled. Nothing left to do. Bye.")
		pagesLeftToCrawl = 0
		break

	print(fromId, newPageToCrawl, end=" ")

	# Delete the page’s from links.
	cursor.execute('''
		DELETE from Links
		WHERE from_id = ?''', ( fromId, )
	)
	
	try:
		document = urlopen(newPageToCrawl, context=ctx)

		html = document.read()
		if document.getcode() != 200 :
			print("Error on page: ",document.getcode())
			cursor.execute('UPDATE Pages SET error=? WHERE url=?', (document.getcode(), newPageToCrawl) )

		if 'text/html' != document.info().get_content_type() :
			print("Ignore non text/html page")
			cursor.execute('DELETE FROM Pages WHERE url=?', ( newPageToCrawl, ) )
			connection.commit()
			continue

		print('('+str(len(html))+')', end=' ')

		soup = BeautifulSoup(html, "html.parser")
	except KeyboardInterrupt:
		print('')
		print('Program interrupted by user...')
		break
	except:
		print("Unable to retrieve or parse page")
		cursor.execute('UPDATE Pages SET error=-1 WHERE url=?', (newPageToCrawl, ) )
		connection.commit()
		continue

	cursor.execute('INSERT OR IGNORE INTO Pages (url, html, new_rank) VALUES ( ?, NULL, 1.0 )', ( newPageToCrawl, ) )
	cursor.execute('UPDATE Pages SET html=? WHERE url=?', (memoryview(html), newPageToCrawl ) )
	connection.commit()

	# Retrieve all of the anchor tags
	tags = soup('a')
	count = 0
	for tag in tags:
		href = tag.get('href', None)
		if ( href is None ) : continue
		# Resolve relative references like href="/contact"
		up = urlparse(href)
		if ( len(up.scheme) < 1 ) :
			href = urljoin(newPageToCrawl, href)
		ipos = href.find('#')
		if ( ipos > 1 ) : href = href[:ipos]
		if ( href.endswith('.png') or href.endswith('.jpg') or href.endswith('.gif') ) : continue
		if ( href.endswith('/') ) : href = href[:-1]
		# print href
		if ( len(href) < 1 ) : continue

		# Check if the URL is in any of the webs
		found = False
		for url in urls:
			if ( href.startswith(url) ) :
				found = True
				break
		if not found : continue

		cursor.execute('INSERT OR IGNORE INTO Pages (url, html, new_rank) VALUES ( ?, NULL, 1.0 )', ( href, ) )
		count = count + 1
		connection.commit()

		cursor.execute('SELECT id FROM Pages WHERE url=? LIMIT 1', ( href, ))
		try:
			pageToCrawl = cursor.fetchone()
			toid = pageToCrawl[0]
		except:
			print('Could not retrieve id')
			continue
		# print fromid, toid
		cursor.execute('INSERT OR IGNORE INTO Links (from_id, to_id) VALUES ( ?, ? )', ( fromId, toid ) )


	print(count)

cursor.close()
