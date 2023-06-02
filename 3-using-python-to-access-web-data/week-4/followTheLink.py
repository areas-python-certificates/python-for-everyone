# Dependencies.
from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl

# Ignore SSL certificate errors.
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Get and follow links.
inputLink = input("Enter a URL: ")
inputPosition = int(input("Enter a position: "))
inputRepeatCount = int(input("Enter a repeat count: "))

# Print the input link.
print(inputLink)

for i in range(inputRepeatCount):
	# Get the beautified links.
	html = urlopen(inputLink, context=ctx).read()
	beautifulHtml = BeautifulSoup(html, "html.parser")
	tags = beautifulHtml("a")

	# Get the link at the specified position and print it.
	outputLink = tags[inputPosition - 1].get("href", None)
	print(outputLink)

	# Update input link for the next loop.
	inputLink = outputLink
