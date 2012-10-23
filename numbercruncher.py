try:
	from configobj import ConfigObj #I'm using configobj instead of the built-in Configeditor as it allows for nested sections and list values
	co = True
except ImportError, e:
	print "ConfigObj module not found - output will not be stored to a file"
	co = False
from ConfigParser import RawConfigParser
from os import curdir, sep, access, R_OK
from decimal import Decimal, InvalidOperation
dot = str(curdir) #The character used by the current os to denote the current folder. Is '.' in Windows
sep = str(sep) #The character used by the current os to denote the demotion to another folder level. Is '/' in Windows
print "What is the name of the file in which the data is located?"
while True : #Infinite loop
	prompt = raw_input(">")
	infile = dot+sep+prompt #Adds ./ in front of the filename to generate a filepath from the scripts directory
	if prompt == "" : #If nothing put in prompt
		infile = dot+sep+"numbers.txt" #For testing purposes - saves me typing it in every time
		break
	elif access(infile, R_OK) : #Checks if given file can be accessed (safer than checking if path exists)
		break #Breaks out of while loop if file can be accessed
	else :
		print "File not found"
print ""		
print "Please type a name for output file"
prompt = raw_input(">")
if prompt == "" : #If nothing put in prompt
	outfile = dot+sep+"output.txt" #For testing purposes - saves me typing it in every time
else :
	outfile = dot+sep+prompt+".txt" #Adds ./ in front of the filename to generate a filepath from the scripts directory
print ""
outfile = ConfigObj(outfile, unrepr=True)
infile = open(infile, 'r') #Opens the given file
indata = infile.readlines()
indata = map(lambda s: s.strip(), indata) #Removes new lines
if not indata[0].isdigit() : #Removed header if exists
	del indata[0]
try :
	indata = map(Decimal, indata) #Converts items in list to long numbers
except ValueError, e : #If a non-number is found then:
	print "File contains non-number characters"
	raw_input("") #Used so that if script is run non-interactively, terminal/prompt will not imediately close and you can read the error message
	exit(0) #Forces exit
print indata, "\n"
print "The lowest number is %s\nWould you like to change it?" %(min(indata))
prompt = raw_input(">").lower() #Captures use input and puts the input into lowercase so 'Yes' will be recognised as 'yes'
if (prompt == '1') or (prompt == 'y') or (prompt == 'yes') or (prompt == 'sure') or (prompt == 'true')  or (prompt == 'ja') or (prompt == 'ok') or (prompt == 'okay') : #Nice and thorough
	print "What would you like to change it to?"
	while True :
		prompt = raw_input(">")
		try : #Will try to turn the input into a long number
			prompt = long(prompt)
			break
		except ValueError, e : #If doing so raises a ValueError then instead of crashing the following is done:
			print "Enter a number to be the new min value"
	minval = prompt
	print "Min value is now %s\n" %(minval)
else :
	minval = min(indata)
	print ""
outfile['Stats'] = {}
outfile['Stats']['min'] = str(minval)
print "The highest number is %s\nWould you like to change it?" %(max(indata))
prompt = raw_input(">").lower()
if (prompt == '1') or (prompt == 'y') or (prompt == 'yes') or (prompt == 'sure') or (prompt == 'true')  or (prompt == 'ja') :
	print "What would you like to change it to?"
	while True :
		prompt = raw_input(">")
		try : #Will try to turn the input into a long number
			prompt = long(prompt)
			break
		except ValueError, e : #If doing so raises a ValueError then, instead of crashing the following is done:
			print "Enter a number to be the new min value"
	maxval = prompt
	print "Min value is now %s\n" %(minval)
else :
	maxval = max(indata)
	print ""
outfile['Stats'] = {}
outfile['Stats']['max'] = str(maxval)
rangeval = maxval-minval
outfile['Stats']['range'] = str(rangeval)
outfile['Stats']['mean'] = int(round(sum(indata)/long(len(indata))))
print "Range of values is %s" %(rangeval)
print "How many classes would you like to sort with?"
while True :
	prompt = raw_input(">")
	try : #Will try to turn the input into a long number
		classtotal = Decimal(prompt)
		break
	except InvalidOperation, e : #If doing so raises a ValueError then, instead of crashing the following is done:
		pass 
classsize = rangeval/classtotal
outfile['Stats']['classtotal'] = str(classtotal)
outfile['Stats']['classsize'] = str(classsize)
outfile.write()

outfile['Classes'] = {}

for element in range(1, classtotal) :
	element = str(element)
	outfile['Classes'][element] = {}
	outfile['Classes'][element]['list'] = []