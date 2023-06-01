# Dependencies.
from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl

# Ignore SSL certificate errors.
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Get and beautify the HTML.
url = input("Enter a URL: ")
html = urlopen(url, context=ctx).read()
beautifulHtml = BeautifulSoup(html, "html.parser")

# Get all the span tags.
tags = beautifulHtml("span")

# Sum the comments.
totalComments = 0
for tag in tags:
	if tag.get("class", None) == ["comments"]:
		totalComments += int(tag.contents[0])

# Print the total comments.
print(totalComments)
