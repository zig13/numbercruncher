from ConfigParser import RawConfigParser
from os import curdir, sep, access, R_OK
dot = str(curdir) #The character used by the current os to denote the current folder. Is '.' in Windows
sep = str(sep) #The character used by the current os to denote the demotion to another folder level. Is '/' in Windows
print "What is the name of the file in which the data is located?"
while True : #Infinite loop
	prompt = raw_input(">")
	infile = dot+sep+prompt #Adds ./ in front of the filename to generate a filepath from the scripts directory
	if prompt == "" : #If nothing put in prompt
		infile = dot+sep+"numbers.txt" #For testing purposes - saves me typing it in every time
		print infile
		break
	elif access(infile, R_OK) : #Checks if given file can be accessed (safer than checking if path exists)
		break #Breaks out of while loop if file can be accessed
	else :
		print "File not found"
infile = open(infile, 'r') #Opens the given file
indata = infile.readlines()
indata = map(lambda s: s.strip(), indata) #Removes new lines
if not indata[0].isdigit() : #Removed header if exists
	del indata[0]
try :
	indata = map(long, indata) #Converts items in list to strings
except ValueError, e : #If a non-number is found then:
	print "File contains non-number characters"
	raw_input("") #Used so that if script is run non-interactively, terminal/prompt will not imediately close and you can read the error message
	exit(0) #Forces exit
print indata, "\n"
print "The lowest number is %s\nWould you like to change it?" %(min(indata))
prompt = raw_input(">").lower() #Captures use input and puts the input into lowercase so 'Yes' will be recognised as 'yes'
if (prompt == '1') or (prompt == 'y') or (prompt == 'yes') or (prompt == 'sure') or (prompt == 'true')  or (prompt == 'ja') : #Nice and thorough
	print "What would you like to change it to?"
	while True :
		prompt = raw_input(">")
		try : #Will try to turn the input into a prompt
			prompt = long(prompt)
			break
		except ValueError, e : #If doing so raises a ValueError then instead of crashing the following is done:
			print "Enter a number to be the new min value"
	minval = prompt
	print "Min value is now %s\n" %(minval)
else :
	minval = min(indata)
	print ""
print "The highest number is %s\nWould you like to change it?" %(max(indata))
prompt = raw_input(">").lower()
if (prompt == '1') or (prompt == 'y') or (prompt == 'yes') or (prompt == 'sure') or (prompt == 'true')  or (prompt == 'ja') :
	print "What would you like to change it to?"
	while True :
		prompt = raw_input(">")
		try : #Will try to turn the input into a prompt
			prompt = long(prompt)
			break
		except ValueError, e : #If doing so raises a ValueError then instead of crashing the following is done:
			print "Enter a number to be the new min value"
	maxval = prompt
	print "Min value is now %s\n" %(minval)
else :
	maxval = max(indata)
	print ""
print "Range of values is %s" %(maxval-minval)