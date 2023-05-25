# 10.2 Write a program to read through the mbox-short.txt and figure out the distribution by hour of the day for each of the messages. You can pull the hour out from the 'From ' line by finding the time and then splitting the string a second time using a colon.
#
# From stephen.marquard@uct.ac.za Sat Jan  5 09:14:16 2008
#
# Once you have accumulated the counts for each hour, print out the counts, sorted by hour as shown below.

# Prompt user for filename.
filename = input("Enter file: ")

# If user doesn’t enter a filename, default to "mbox-short.txt".
if len(filename) == 0: filename = "mbox-short.txt"

# Open file.
file = open(filename)

# Create empty dictionary.
emailsSentByHourOfDay = dict()

# Loop through each line in the file.
for line in file:
  # If the line starts with “From ”,
	# split the line until you get the hour of the day,
	# and add it to the hourOfTheDay dictionary.
  if line.startswith("From "):
    words = line.split()
    time = words[5]
    hour = time.split(":")[0]  
    emailsSentByHourOfDay[hour] = emailsSentByHourOfDay.get(hour, 0) + 1

# Create empty list.
emailsSentByHourOfDaySorted = list()

# Loop through each key-value pair in the dictionary.
for hour, sends in emailsSentByHourOfDay.items():
  emailsSentByHourOfDaySorted.append((hour, sends))

# Sort the list by hour.
emailsSentByHourOfDaySorted.sort()

# Print the list.
for hour, sends in emailsSentByHourOfDaySorted:
  print(hour, sends)
