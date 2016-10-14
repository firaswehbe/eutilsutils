#!/usr/bin/env python

from Bio import Entrez
import csv
import pandas as pd
import sys
import os.path

# General script bookkeeping and hygeine

print (sys.argv)

if len(sys.argv) < 3:
    sys.exit('Need to specify 2 arguments')

pmidfile = sys.argv[1]
if not os.path.exists(pmidfile):
    sys.exit('Input file "{0}" does not exist'.format(pmidfile))

csvfile = sys.argv[2]
if os.path.exists(csvfile):
    sys.exit('Output file "{0}" already exist, cannot overwrite'.format(csvfile))


# Defining the columns, eSummary is flat, so in general no need to fetch data 
# from deep nested structures

cols =[
    'pmid','pmc'
    ]

outframe = pd.DataFrame( columns = cols )


# Mapping function from the eSummary() data structure to the columns above
# TODO: This is not used now, I put it here so we can use parse and iterator for
# large results

def extractSummary( esummobject ):
    myextract = dict()
    myextract['pmid'] = esummobject['Id']
    myextract['pmc'] = None
    if 'ArticleIds' in esummobject.keys():
        if 'pmc' in esummobject['ArticleIds'].keys(): 
            myextract['pmc'] = esummobject['ArticleIds']['pmc']
    return myextract


# Expect this to run in a terminal, so show dynamic results in bold red
def makeRed(myinput):
    return "\x1b[0;31m"+str(myinput)+"\x1b[0m"

def makeYellow(myinput):
    return "\x1b[0;33m"+str(myinput)+"\x1b[0m"


# Need to tell the NLM who you are when you access e-utils
Entrez.email = 'firaswehbe@users.noreply.github.com'
Entrez.tool = 'github.com/firaswehbe/eutilsutils/scripts/pmid2csv.py'

# Read a list of pubmed ids into a list for use in testing scripts
testpmids = list()
fh = open(pmidfile,'r')
for x in fh:
    testpmids.append(x.strip())
fh.close()

# Uncomment below in verbose flag
'''
print("Read ids from {0}: {1}\n..."\
        .format(makeYellow(pmidfile),makeRed(len(testpmids))))
'''

# Run an Entrez.post
# Uncomment below in verbose flag
#print("Sending {0} from the pmids file\n...".format(makeYellow('Entrez.epost()')))
myhandle = Entrez.epost( 'pubmed', id=','.join(testpmids) )
myresult = Entrez.read( myhandle )
mywebenv = myresult['WebEnv']
myquerykey = myresult['QueryKey']

# Uncomment below in verbose flag
'''
print("WebEnv: {0}\nquery_key: {1}\n..."\
        .format(makeRed(mywebenv),makeRed(myquerykey)))
'''

# Run an Entrez.esummary
# Uncomment in verbose mode
#print("Requesting {0} based on the epost\n...".format(makeYellow('Entrez.esummary()')))
myhandle = Entrez.esummary( db='pubmed', webenv=mywebenv, query_key=myquerykey)
myresult = Entrez.read( myhandle )
# Uncomment in verbose mode
#print("Got response of length: {0}".format(makeRed(len(myresult))))
for x in myresult:
    outframe = outframe.append( pd.Series( extractSummary(x) ), ignore_index=True )

# Write to csvfile
# Uncomment in verbose mode
#print("Writing to {0}\n...".format(makeRed(csvfile)))
outframe.to_csv(csvfile, quoting=csv.QUOTE_ALL, index=False)

