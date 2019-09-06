#!/usr/bin/env python

if __name__ != '__main__':
    import sys
    sys.exit("This script cannot be imported, only run from command line")

import pandas as PD
import sqlalchemy as SA
import eutilsconfig as EC
import logging
from Bio import Entrez as en
import argparse
import sys

# Initialize loggers, Entrez, db, 
myargparser = argparse.ArgumentParser(description='Append or update database based on list of pmids')
myargparser.add_argument("--logfile", help="Where data from this script are logged", default="log/scripts.log")
myargparser.add_argument("--input", help="Path to the file where the pmids are stored", default="input/fhw.pmids")
myargparser.add_argument("--output", help="Path to the file where the esummaries will be stored", default="output/fhw.csv")
myargs = myargparser.parse_args()

en.email = 'firas.wehbe' + '@' + 'northwestern.edu'
logging.basicConfig(filename=myargs.logfile,level=logging.DEBUG,format='%(asctime)s %(levelname)s:%(filename)s:%(lineno)s:%(message)s')
myengine = SA.create_engine(EC.myenginestr)
mymeta = SA.MetaData(myengine)
mymeta.reflect(only=['esummaries'])
myesummaries = mymeta.tables['esummaries']

logging.info('----- new pmid2psql.py execution -----')

# Read pmids from file
pmids = PD.read_csv(myargs.input,
        header = None, names = ['pmid'], dtype='str')
logging.info('Reading {0} PMIDS from "{1}"'.format( len(pmids), myargs.input ))
print('Reading {0} PMIDS from "{1}"'.format( len(pmids), myargs.input ))

# Fetch the pmids from pubmed eutils using esummary
logging.info('Attempting to fetch eSummaries from PubMed for {0} PMIDs'.format(len(pmids.pmid)))
esum_records = en.read( en.esummary( db='pubmed', id = ','.join(pmids.pmid) ) )
esum_list = []
logging.info('Fetched {0} PMID records from PubMed eSummary'.format(len(esum_records)))
print('Fetched {0} PMID records from PubMed eSummary'.format(len(esum_records)))

# Parse and load into a pandas data frame
for record in esum_records:
    esum_list.append((
            record['Id'],
            ','.join(record['AuthorList']),
            record['Title'],
            record['Source'],
            record['SO']
            ))
esum_df = PD.DataFrame(esum_list,columns=['pmid','authors','title','source','so'])

#Write to CSV
esum_df.to_csv(myargs.output,index=False)
logging.info('Wrote details on {0} PMIDS to "{1}"'.format(len(pmids.pmid), myargs.output))
print('Wrote details on {0} PMIDS to "{1}"'.format(len(pmids.pmid), myargs.output))

#Check for existing records
myconn = myengine.connect()
s = SA.sql.select( [myesummaries.c.pmid] ).where( myesummaries.c.pmid.in_(pmids.pmid) )
myexisting = PD.read_sql(s,myconn)
logging.warning('Found {0} existing PMIDS in the "esummaries" table.'.format( len(myexisting) ))
print('Found {0} existing PMIDS in the "esummaries" table.'.format( len(myexisting) ))
if myexisting.size >0:
    mydel = myconn.execute( myesummaries.delete().where( myesummaries.c.pmid.in_(myexisting.pmid) ) )
    logging.warning('Deleted {0} PMIDS in the "esummaries" table.'.format( mydel.rowcount ))
    print('Deleted {0} PMIDS in the "esummaries" table.'.format( mydel.rowcount ))

# Write to DB
esum_df.to_sql('esummaries',myconn,if_exists='append',index=False)
logging.info('Inserted {0} PMIDS into the "esummaries" table.'.format( len(esum_df) ) )
print('Inserted {0} PMIDS into the "esummaries" table.'.format( len(esum_df) ) )

