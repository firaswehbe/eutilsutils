#!/usr/bin/env python

from Bio import Entrez
from Bio import Medline
import sys

# Need to tell the NLM who you are when you access e-utils
Entrez.email = 'firaswehbe@users.noreply.github.com'
Entrez.tool = 'github.com/firaswehbe/eutilsutils/scripts/bioPythonHelloWorld.py'

# Read a list of pubmed ids into a list for use in testing scripts
pmidfile = 'input/fhw.pmids'
testpmids = list()
fh = open(pmidfile,'r')
for x in fh:
    testpmids.append(x.strip())
fh.close()
print("Read ids from {0}: {1}\n..."\
        .format(makeYellow(pmidfile),makeRed(len(testpmids))))

# Run an Entrez.post
print("Sending {0} from the pmids file\n...".format(makeYellow('Entrez.epost')))
myhandle = Entrez.epost( 'pubmed', id=','.join(testpmids) )
myresult = Entrez.read( myhandle )
mywebenv = myresult['WebEnv']
myquerykey = myresult['QueryKey']
print("WebEnv: {0}\nquery_key: {1}\n..."\
        .format(makeRed(mywebenv),makeYellow(myquerykey)))

# Run an Entrez.esummary
print("Requesting {0} based on the epost\n...".format(makeYellow('Entrez.esummary()')))
myhandle = Entrez.esummary( db='pubmed', webenv=mywebenv, query_key=myquerykey)
myresult = Entrez.read( myhandle )
print("Got response of length: {0}".format(makeRed(len(myresult))))
for x in myresult:
    print("{0}\t{1}\t{2}\t{3}"\
            .format(x['Id'],x['Title'][0:40],x['Source'],x['SO']))
print("...")

