#!/usr/bin/env python

import textwrap
import yaml
def interval(f,current,duration, pct):
	f.write(textwrap.dedent(
		"""
		{1} {0}
		{2} {0}""".format(pct,current,current+duration)))
	return current + duration

def handle_step(f,c,i):
	print(i)
	return interval(f,c,i[1]['duration'],i[1]['ftp-pct'])



with open("over-under-intervalle.yaml", 'r') as stream:
	
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
