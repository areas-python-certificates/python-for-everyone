# 9.4 Write a program to read through the mbox-short.txt and figure out who has sent the greatest number of mail messages. The program looks for 'From ' lines and takes the second word of those lines as the person who sent the mail. The program creates a Python dictionary that maps the sender's mail address to a count of the number of times they appear in the file. After the dictionary is produced, the program reads through the dictionary using a maximum loop to find the most prolific committer.

filename = input("Enter filename: ")

if len(filename) == 0: filename = "mbox-short.txt"

fileHandle = open(filename)

emailsSent = dict()

for line in fileHandle:
	if line.startswith("From "):
		sender = line.split()[1]
		emailsSent[sender] = emailsSent.get(sender, 0) + 1

mostProlificSender = None

for sender in emailsSent:
	if mostProlificSender is None or emailsSent[sender] > emailsSent[mostProlificSender]:
		mostProlificSender = sender

print(mostProlificSender, emailsSent[mostProlificSender])
