#!/usr/bin/env python

import pandas

from Bio import Entrez as en
en.email = 'firas.wehbe' + '@' + 'northwestern.edu'

pmids = pandas.read_csv('input/fhw.pmids',
        header = None, names = ['pmid'], dtype='str')

#mydata = en.read( en.esummary( db='pubmed', id = ','.join(testpmids) ) )


