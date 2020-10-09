"""
Workflow:
1. Take filename as input (i.e., `scriptname filename`)
2. Read header and save as array
3. Output header and first three lines as example text
4. Prompt for header choice and values to look for
5. Display one sample line for each value prompted for
6. Sort the file by the header choice
7. Output single CSV based off of x header values
"""

import csv
import sys
import io
import operator
from operator import itemgetter

# Accept filename as input and assign to variable
filename = sys.argv[1]

# Open file
with io.open(filename, newline='') as csv_file:
	dialect = csv.Sniffer().sniff(csv_file.read(4096))
	csv_file.seek(0)
	csv_reader = csv.reader(csv_file, dialect)
	
	header = []
	line_count = 0

	for row in csv_reader:
		if line_count == 0:
			# Read header and save as array	
			for column in row:
				header.append(column)
			# Output header and first three lines as example text
			line_count += 1
			blank_column = [None] * len(header)
		else:
			for i,column in enumerate(row):
				if column != "":
					blank_column[i] = 1
		
	# Check for empty columns and remove them to prevent later index errors also delete the column from the headers.
	for i,column in enumerate(blank_column):
		if column == None:
			header[i]=None
			

	# Ask for header choice
	print('\nWHICH HEADER WOULD YOU LIKE TO USE TO SPLIT? \n')
	
	for i,column in enumerate(header):
		if column != None:
			printValue = str(i)
			printValue += ". "
			printValue += header[i]
			print(printValue)

	# fix the count here
	header_choice = int(input('Please enter a value between 0 and {}: '.format(len(header))))
	

with io.open(filename, newline='') as csv_file:
	csv_reader = csv.reader(csv_file, dialect)
	
	# Sort the file based off of header choice
	sortedlist = sorted(csv_reader, key=lambda row: row[header_choice], reverse=True)
	
	choices = []

	line_count = 0
	for row in sortedlist:
		# capture each value and discard if non-unique
		# print remaining values
		choices.append(row[header_choice])
		line_count += 1
		if line_count == len(sortedlist):
			break

	# Display list of possible values and prompt for choices
	print('\nWHICH VALUE(S) DO YOU WANT? \n')
	
	# Remove the header value from this list.
	del choices[0]
	#choices.pop(0)
	
	# Make the list unique using set
	unique_choices = set(choices)
	unique_value = []
	choices = list(unique_choices)
	
	# Set the count to 0
	count = 0
	
	# Loop through the options menu until the user has picked all values they want or there are none remaining
	while count < len(unique_choices):
		# Set the choice_count to 0
		choice_count = 0
		for value in unique_choices:
			printValue = str(choice_count)
			printValue += ". "
			printValue += value
			print(printValue)
			choice_count += 1
		print ('{}. ALL'.format(choice_count))
		if count > 0:
			choice_count += 1
			print ('{}. No more'.format(choice_count))
	
		# Extend this to allow selection of all values
		unique_value.append(int(input('Please enter a value between 0 and {}: '.format(choice_count))))
	
		if unique_value[count] == len(unique_choices):
			print("")
			print("you selected all")
			count = len(unique_choices)
			# Make unique_value contain all options.
			unique_value = []
			for choice in choices:
				unique_value.append(choices.index(choice))
		elif unique_value[-1] == (len(unique_choices)+1):
			print("")
			print("You are done selecting")
			del unique_value[-1]
			count = len(unique_choices)
		else:
			# print a single matching row
			print('You selected: {}'.format(choices[unique_value[-1]]))
			count += 1
	
		
	# Display a sample line that matches each value to verify it's working
	print(header)
	for value in unique_value:
		# Use the header_choice variable to find the row that needs to be sorted by.
		# For example if the message_type is chosen, return the header, then return each record that has the matching value.
		for row in sortedlist:
			if row[header_choice] == choices[value]:
				print(row)
				break
	
	# Split into a single CSV based off of the values chosen
	with open('split.csv', 'w') as newfile:
		for value in unique_value:	
			wr = csv.writer(newfile, quoting=csv.QUOTE_ALL)
			# Output the header to said new file
			wr.writerow(header)
			# then output every matching row to the same file
			for row in sortedlist:
				if row[header_choice] == choices[value]:
					wr.writerow(row)
