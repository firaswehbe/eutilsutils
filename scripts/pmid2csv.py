#!/usr/bin/env python

from Bio import Entrez
from Bio import Medline
import sys
import os.path

if len(sys.argv) < 3:
    sys.exit('Need to specify 2 arguments')

pmidfile = sys.argv[1]
if not os.path.exists(pmidfile):
    sys.exit('Input file "{0}" does not exist'.format(pmidfile))

csvfile = sys.argv[2]
if os.path.exists(csvfile):
    sys.exit('Output file "{0}" already exist, cannot overwrite'.format(csvfile))


# Need to tell the NLM who you are when you access e-utils
Entrez.email = 'firaswehbe@users.noreply.github.com'
Entrez.tool = 'github.com/firaswehbe/eutilsutils/scripts/bioPythonHelloWorld.py'

# Read a list of pubmed ids into a list for use in testing scripts
testpmids = list()
fh = open(pmidfile,'r')
for x in fh:
    testpmids.append(x.strip())
fh.close()
#print("Read ids from {0}: {1}\n..."\
#        .format(makeYellow(pmidfile),makeRed(len(testpmids))))

# Run an Entrez.post
print("Sending {0} from the pmids file\n...".format('Entrez.epost'))
myhandle = Entrez.epost( 'pubmed', id=','.join(testpmids) )
myresult = Entrez.read( myhandle )
mywebenv = myresult['WebEnv']
myquerykey = myresult['QueryKey']
#print("WebEnv: {0}\nquery_key: {1}\n..."\
#        .format(makeRed(mywebenv),makeYellow(myquerykey)))

# Run an Entrez.esummary
print("Requesting {0} based on the epost\n...".format('Entrez.esummary()'))
myhandle = Entrez.esummary( db='pubmed', webenv=mywebenv, query_key=myquerykey)
myresult = Entrez.read( myhandle )
print("Got response of length: {0}".format(len(myresult)))
for x in myresult:
    print("{0}\t{1}\t{2}\t{3}"\
            .format(x['Id'],x['Title'][0:40],x['Source'],x['SO']))
print("...")

print sys.argv
