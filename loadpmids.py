#!/usr/bin/env python

#######################################
# General app framework set up
# Read the global configuration

import configparser
config = configparser.ConfigParser()
config.read('config/config.ini')

#######################################
# DB Setup
# Use this to create engine, session, and Base

import sqlalchemy as SA
import sqlalchemy.orm as SAORM

#should use proper config module or something
myengineurl = 'postgresql://eutilsutils_user:@localhost:5432/eutilsutils_db'
myengine = SA.create_engine(myengineurl)
# look into scoped_session
mysessionmaker = SAORM.sessionmaker(myengine)
Base = SAORM.declarative_base()


#######################################
# Model definitions
# Should use DB set up above to have access to Base

class PMPaper(Base):
    __tablename__ = 'pm_paper'

    id = SA.Column(SA.Integer, primary_key=True)
    title = SA.Column(SA.String(500))
    pdat = SA.Column(SA.Date)
    edat = SA.Column(SA.Date)

#######################################
# Biopython Entrez stuff

from Bio import Entrez as en
print(f"email = {config['pubmed']['email']} | api_key = {config['pubmed']['api_key']}")
en.email = config['pubmed']['email']
en.api_key = config['pubmed']['api_key']

#######################################
# Entrez parsing utilities

class PMPaperLoadError (RuntimeError):
    """Thrown when reading PM records that don't map to our schema"""
    pass

def loadEfetch2PMPapers(efetch_result, skip_existing=True):
    """
    Should return a list indicating parsed/loaded or retrieved instances in database
    """
    if getattr(efetch_result,'tag',None) != 'PubmedArticleSet':
        raise PMPaperLoadError('Wrong root tag for efetch')
    mypmpaper_list = []
    with mysessionmaker.begin() as mysession:
        for mypmarticle in efetch_result['PubmedArticle']:
            # These two nested keys should be required per DTD
            # If not, a raised key error should break the session
            mymedlinecitation = mypmarticle['MedlineCitation']
            mypmid = str(mymedlinecitation['PMID'])
            myPMPaper = mysession.get(PMPaper,mypmid)
            if myPMPaper is not None and skip_existing:
                # We just did a database look up; keep track of cost in large batches
                # If record in database add it to container, print message, and skip
                mypmpaper_list.append((mypmid,'in db - loaded from db only'))
                print(f"PMID: {mypmid} exists in the database, skipping...")
                continue
            elif myPMPaper is None:
                mypmpaper_list.append((mypmid,'not in db - parsed and inserted'))
                myPMPaper = PMPaper(id=mypmid)
            else:
                mypmpaper_list.append((mypmid,'in db - parsed and updated'))
            # Session.merge() returns the new object loaded/created in session, use that going forward
            myPMPaper = mysession.merge(myPMPaper) 
            myPMPaper.title = mymedlinecitation['Article']['ArticleTitle']
            # Add other attributes later


    # Should commit session or rollback at the end of the begin() context
    # Should close the session as well given the construct used to start the context

    return mypmpaper_list


#######################################
# Do the thing

import rich

with en.esearch(db='pubmed', term='wehbe f[au]', usehistory='y') as sh1:
    result1 = en.read(sh1)
    print(f"Search #{result1['QueryKey']} returns {result1['Count']} / WebEnv = {result1['WebEnv']}")
    mywebenv = result1['WebEnv']
    myquerykey = result1['QueryKey']

with en.efetch(db='pubmed', query_key=myquerykey, WebEnv=mywebenv, retmax=50) as sh2:
    result2 = en.read(sh2)

thepaperinstances = loadEfetch2PMPapers(result2)
    

