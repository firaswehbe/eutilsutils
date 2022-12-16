#!/usr/bin/env python

import rich
import rich.pretty
import eutilsutils
import eutilsutils.parser
app = eutilsutils.EutilsUtils()
import time

mylog = []

def append_log(theresult):
    mylog.append((
        theresult['Count'],
        theresult['WebEnv'],
        theresult['QueryKey']
    ))

with app.en.esearch(db='pubmed', term='Heart Failure', usehistory='y') as sh:
    result = app.en.read(sh)
    append_log(result)

with app.en.esearch(db='pubmed', term='artificial intelligence OR machine learning OR deep learning', usehistory='y', WebEnv=result['WebEnv']) as sh:
    result = app.en.read(sh)
    append_log(result)

with app.en.esearch(db='pubmed', term='(#1) AND (#2) AND english[la]', usehistory='y', WebEnv=result['WebEnv']) as sh:
    result = app.en.read(sh)
    append_log(result)

rich.pretty.pprint(mylog)

step = 500
load_log = []
for i in range(0,int(result['Count']),step):
    rich.print(f"Requesting {i} to {i+step} ...", end=" ")
    with app.en.efetch(db='pubmed', query_key=result['QueryKey'], WebEnv=result['WebEnv'], retstart=i, retmax=step) as fh:
        fetched = app.en.read(fh)
    rich.print(f"Parsing {len(fetched['PubmedArticle'])}",end=" ")
    load_log.extend(eutilsutils.parser.loadEfetch2PMPapers(app,fetched,False))
    rich.print(f"Parsed")
    time.sleep(3)
    
