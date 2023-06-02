# Dependencies.
import urllib.request, urllib.parse, urllib.error
import xml.etree.ElementTree as et

# Get XML.
url = input('Enter URL: ')
urlHandle = urllib.request.urlopen(url)
xml = urlHandle.read()

# Parse XML.
xmlTree = et.fromstring(xml)
commentElements = xmlTree.findall(".//count")

# Sum the total number of comments.
totalComments = 0

for commentElement in commentElements:
	totalComments += int(commentElement.text)

print(totalComments)
