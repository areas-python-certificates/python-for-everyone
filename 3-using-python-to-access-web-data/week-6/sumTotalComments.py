# Dependencies.
import urllib.request, urllib.parse, urllib.error
import json

# Get JSON.
url = input("Enter URL: ")
urlHandle = urllib.request.urlopen(url)
json = json.loads(urlHandle.read())

# Sum the total number of comments.
totalComments = 0

for commentObject in json["comments"]:
	totalComments += int(commentObject["count"])

print(totalComments)
