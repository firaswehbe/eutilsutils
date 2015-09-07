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
Entrez.tool = 'firaswehbe@github:/eutilsutils'

print("Setting up email and tools as:\n{0}\n{1}\n...".format(Entrez.email, Entrez.tool))
print("Running {0}\n...".format(makeYellow("Entrez.einfo( db='pubmed' )")))

myhandle = Entrez.einfo( db='pubmed' )
myresult = Entrez.read( myhandle )
print("Date of last update: {0}".format(makeRed(myresult['DbInfo']['LastUpdate'])))
print("Description of PubMed: {0}".format(makeRed(myresult['DbInfo']['Description'])))
print("Number of records in PubMed: {0}".format(makeRed(myresult['DbInfo']['Count'])))
