from ConfigParser import RawConfigParser
from os import curdir, sep, access, R_OK
dot = str(curdir) #The character used by the current os to denote the current folder. Is '.' in Windows
sep = str(sep) #The character used by the current os to denote the demotion to another folder level. Is '/' in Windows
print "What is the name of the file in which the data is located?"
while True :
	prompt = raw_input(">")
	infile = dot+sep+prompt
	if access(infile, R_OK) :
		break
	else :
		print "File not found"
infile = open(infile, 'r')