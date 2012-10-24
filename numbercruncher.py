from ConfigParser import RawConfigParser
try:
	from configobj import ConfigObj #I'm using configobj instead of the built-in Configeditor as it allows for nested sections and list values
	outengine = "obj"
except ImportError, e:
	print "ConfigObj module not found - ConfigParser will be used instead\n"
	outengine = "parser"
	outfile = RawConfigParser()
from os import curdir, sep, access, R_OK
from decimal import Decimal, InvalidOperation
from math import ceil

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
	outloc = dot+sep+"output.txt" #For testing purposes - saves me typing it in every time
else :
	outloc = dot+sep+prompt+".txt" #Adds ./ in front of the filename to generate a filepath from the scripts directory
print ""

if outengine == "obj" :
	outfile = ConfigObj(outloc, unrepr=True)
	
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
	
rangeval = maxval-minval
print "Range of values is %s" %(rangeval)
print "How many classes would you like to sort with?"
while True :
	prompt = raw_input(">")
	try : #Will try to turn the input into a long number
		classtotal = Decimal(prompt)
		break
	except InvalidOperation, e : #If doing so raises InvalidOperation then, instead of crashing the following is done:
		pass 
classrange = rangeval/classtotal
meanval = int(round(sum(indata)/long(len(indata))))

if outengine == "obj" :
	outfile['Stats'] = {}
	outfile['Stats']['min'] = str(minval)
	outfile['Stats']['max'] = str(maxval)
	outfile['Stats']['range'] = str(rangeval)
	outfile['Stats']['mean'] = int(round(sum(indata)/long(len(indata))))
	outfile['Stats']['classtotal'] = str(classtotal)
	outfile['Stats']['classrange'] = str(classrange)
	outfile['Classes'] = {}
	for element in range(1, classtotal) :
		outfile['Classes'][str(element)] = {}
		outfile['Classes'][str(element)]['list'] = []
	outfile.write()
else :
	outfile.add_section('stats')
	outfile.set('stats', 'minval', minval)
	outfile.set('stats', 'maxval', maxval)
	outfile.set('stats', 'range', rangeval)
	outfile.set('stats', 'mean', meanval)
	outfile.set('stats', 'classtotal', classtotal)
	outfile.set('stats', 'classrange', classrange)
	outfile.add_section('classtotals')
	for element in range(1, classtotal) :
		exec("class%slist = []" %(element))
	for element in indata :
		numclass = long(ceil(element/classrange))
		exec("class%slist.append(element)" %(numclass))
	for element in range(1, classtotal) :
		exec("classtotal = len(class%list)" %(element))
		outfile.set('classtotals', element, classtotal)
	with open(outloc, 'w') as fileout :
		fileout.write(outfile)