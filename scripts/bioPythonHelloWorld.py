#!/usr/bin/env python

# THis is a quick test to see if BioPython is working

# All the eutilsutils code requires BioPython
# TODO: handle fail

from Bio import Entrez
import sys

# Expect this to run in a terminal, so show dynamic results in bold red
def makeRed(myinput):
    return "\x1b[0;31m"+str(myinput)+"\x1b[0m"

def makeYellow(myinput):
    return "\x1b[0;33m"+str(myinput)+"\x1b[0m"

# Some bookkeeping things. Show what version of Python this script is running
print("Printing python version\n...")
print("{0}".format(makeYellow(sys.version)))

# Need to tell the NLM who you are when you access e-utils
Entrez.email = 'firaswehbe@users.noreply.github.com'
Entrez.tool = 'github.com/firaswehbe/eutilsutils/scripts/bioPythonHelloWorld.py'

print("Setting up email and tools as:\nEntrez.email: {0}\nEntrez.tool: {1}\n..."\
        .format(makeYellow(Entrez.email), makeYellow(Entrez.tool)))
print("Running {0}\n...".format(makeYellow("Entrez.einfo( db='pubmed' )")))

myhandle = Entrez.einfo( db='pubmed' )
myresult = Entrez.read( myhandle )
print("Date of last update: {0}".format(makeRed(myresult['DbInfo']['LastUpdate'])))
print("Description of PubMed: {0}".format(makeRed(myresult['DbInfo']['Description'])))
print("Number of records in PubMed: {0}\n...".format(makeRed(myresult['DbInfo']['Count'])))

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

# Run an Entrez.esearch
print("Running {0} using the term {1}\n..."\
        .format(makeYellow('Entrez.esearch()'),makeYellow('wehbe f[au]')))
myhandle = Entrez.esearch( db='pubmed', term='wehbe f[au]', usehistory='y', webenv=mywebenv)
myresult = Entrez.read( myhandle )
mywebenv = myresult['WebEnv']
myquerykey = myresult['QueryKey']
print("Got response with the following attributes:")
print("Count: {0}".format(makeRed(myresult['Count'])))
print("RetStart: {0}\tRetMax: {1}".format(makeRed(myresult['RetStart']),makeRed(myresult['RetMax'])))
print("IdList (just count): {0}".format(makeRed(len(myresult['IdList']))))
print("QueryTranslation: {0}".format(makeRed(myresult['QueryTranslation'])))
print("TranslationStack: {0}".format(makeRed('** not shown **')))
print("TranslationSet: {0}".format(makeRed('** not shown **')))
print("WebEnv: {0}\nquery_key: {1}\n..."\
        .format(makeRed(mywebenv),makeYellow(myquerykey)))
print("...")

# Run an Entrez.efetch
print("Requesting {0} based on the esearch\n...".format(makeYellow('Entrez.efetch()')))
myhandle = Entrez.efetch( db='pubmed', webenv=mywebenv, query_key=myquerykey, retmode='xml' ) #Default is JSON!
myresult = Entrez.read( myhandle )
print("Got response of length: {0}".format(makeRed(len(myresult))))
