from ConfigParser import RawConfigParser
outfile = RawConfigParser()

from os import curdir, sep, access, R_OK, startfile, path, remove
from decimal import Decimal, InvalidOperation
from math import ceil

prompt = raw_input("What is the name of the file in which the data is located?\n>")
infile = "./"+prompt

prompt = raw_input("\nPlease type a name for output file\n>")
outloc = "./"+prompt+".txt"

infile = open(infile, 'r') #Opens the given file
indata = infile.readlines()

indata = map(lambda s: s.strip(), indata) #Removes new lines
if not indata[0].isdigit() : #Removed header if exists
	del indata[0]
indata = map(Decimal, indata) #Converts items in list to long numbers
totalval = len(indata)

print "\nThe lowest number is %s\nPress enter to leave alone or input a number to change" %(min(indata))
prompt = raw_input(">")
if prompt.isdigit() :
	minval = long(prompt)
	print "Min value is now %s" %(minval)
else :
	minval = min(indata)

print "\nThe highest number is %s\nPress enter to leave alone or input a number to change" %(max(indata))
prompt = raw_input(">")
if prompt.isdigit() :
	maxval = long(prompt)
	print "Max value is now %s\n" %(maxval)
else :
	maxval = max(indata)
	print ""
	
rangeval = maxval-minval
print "Range of values is %s\nHow many classes would you like to sort with?" %(rangeval)
prompt = raw_input(">")
totalclasses = long(prompt)

outfile.add_section('ClassSizes') #Creates new empty section in the virtual ini file

classes = [] #Creates an empty list called classes

for element in range(totalclasses+1) : #Range creates a list of numbers from 0 to the number of classes. 0 is used for excluded values and the others represent a class each
	classes.append([]) #For every class plus zero, creates an empty list in the list 'classes'
for element in indata : #For every number in numbers file
	if element == minval : #Bit hacky but enables the math to be a lot simpler
		numclass = 1
	elif (element < minval) or (element > maxval) : #If outside range (will only occur if user changes range)
		numclass = 0 #Will result in number being added to the excluded list
	else :
		numclass = int(ceil((element-minval)/(rangeval/totalclasses))) #The MATHS 
	classes[numclass].append(element)
for element in range(totalclasses) : #This range starts at 1 thus excluding the excluded value list
	outfile.set('ClassSizes', str(int(minval+(element*(rangeval/totalclasses)))), len(classes[element+1])) #Counts values in each class list
if len(classes[0]) > 0 : #If some values were excluded
	outfile.add_section('Stats')
	outfile.set('Stats', 'excluded_values', len(classes[0]))
with open(outloc, 'w') as fileout :
	outfile.write(fileout)
raw_input("Crunching Completed Succesfully\nPress enter to view output") #Made raw_input rather than pritn so dosn't imediately close on finish
startfile(path.normpath(outloc)) #Opens output with default text editor