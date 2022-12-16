#!/usr/bin/env python

import rich.pretty
import eutilsutils
import eutilsutils.parser
app = eutilsutils.EutilsUtils()

with app.en.esearch(db='pubmed', term='wehbe f[au]', usehistory='y') as sh1:
    result1 = app.en.read(sh1)
    print(f"Search #{result1['QueryKey']} returns {result1['Count']} / WebEnv = {result1['WebEnv']}")

with app.en.efetch(db='pubmed', query_key=result1['QueryKey'], WebEnv=result1['WebEnv'], retmax=50) as sh2:
    result2 = app.en.read(sh2)

thepaperinstances = eutilsutils.parser.loadEfetch2PMPapers(app,result2,False)

rich.pretty.pprint(thepaperinstances)
    

