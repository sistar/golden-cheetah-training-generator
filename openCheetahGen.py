#!/usr/bin/env python

import textwrap
import yaml
import sys, getopt

def interval(f,current,duration, pct):
	f.write(textwrap.dedent(
		"""
		{1} {0}
		{2} {0}""".format(pct,current,current+duration)))
	return current + duration

def handle_step(f,c,i):
	print(i)
	return interval(f,c,i[1]['duration'],i[1]['ftp-pct'])


def generate(inputfile):
	with open(inputfile, 'r') as stream:

	    try:
	        data = yaml.load(stream)
	        f=open(data['file-name'],'w')
	        f.write("""
	[COURSE HEADER]
	VERSION = 2
	UNITS = METRIC
	DESCRIPTION = {0}
	FILE NAME = {1}
	MINUTES PERCENTAGE
	[END COURSE HEADER]
	[COURSE DATA]
		""".format(data['description'],data['file-name']))

	        d2 = map(len, data)
	        c = 0
	        for x in data['plan']:

	        	for i in x.items():
	        		if(i[0] == 'repeat'):
	        			print("repeat: " +str(i[1]))
	        			for rep in range(0,i[1]['times']):
	        				for s in i[1]['steps']:
	        						for a in s.items():
	        							c = handle_step(f,c,a)
	        		else:
	        			print ("step:" + str(i))
	        			c = handle_step(f,c,i)

	    except yaml.YAMLError as exc:
	        print(exc)
	f.write("""
	[END COURSE DATA]
		""")

	f.close

def main(argv):
   inputfile = ''
   outputfile = ''
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile="])
   except getopt.GetoptError:
      print 'openCheetahGen.py -i <inputfile>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'openCheetahGen.py -i <inputfile>'
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
   print 'Input file is "', inputfile
   print 'Output file is "', outputfile
   sys.exit(2)
   generate(inputfile)

if __name__ == "__main__":
   main(sys.argv[1:])
