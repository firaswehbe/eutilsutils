#!/usr/bin/env python

if __name__ != '__main__':
    import sys
    sys.exit("This script cannot be imported, only run from command line")

import pandas
import sqlalchemy as SA
import eutilsconfig as EC
import logging
from Bio import Entrez as en
import argparse

# Initialize loggers, Entrez, db, 
myargparser = argparse.ArgumentParser(description='Append or update database based on list of pmids')
myargparser.add_argument("--logfile", help="Where data from this script are logged", default="log/scripts.log")
myargparser.add_argument("--input", help="Path to the file where the pmids are stored", default="input/fhw.pmids")
myargparser.add_argument("--output", help="Path to the file where the esummaries will be stored", default="output/fhw.csv")
myargs = myargparser.parse_args()

en.email = 'firas.wehbe' + '@' + 'northwestern.edu'
logging.basicConfig(filename=myargs.logfile,level=logging.DEBUG,format='%(asctime)s %(levelname)s:%(filename)s:%(lineno)s:%(message)s')
myengine = SA.create_engine(EC.myenginestr)

# Read pmids from file
pmids = pandas.read_csv(myargs.input,
        header = None, names = ['pmid'], dtype='str')

# Fetch the pmids from pubmed eutils using esummary
logging.info('Attempting to fetch eSummaries for the following {0} PMIDs:{1}'.format(len(pmids.pmid),','.join(pmids.pmid)))
esum_records = en.read( en.esummary( db='pubmed', id = ','.join(pmids.pmid) ) )
esum_list = []
logging.info('Fetched {0} PMIDS from esummary'.format(len(esum_records)))

# Parse and load into a pandas data frame
for record in esum_records:
    esum_list.append((
            record['Id'],
            ','.join(record['AuthorList']),
            record['Title'],
            record['Source'],
            record['SO']
            ))
esum_df = pandas.DataFrame(esum_list,columns=['pmid','authors','title','source','so'])

#Write to CSV
logging.info('Wrote {0} PMIDS to csv file'.format(len(pmids.pmid)))
esum_df.to_csv(myargs.output,index=False)

#Check for existing records
    

"""
# Write to DB
#esym_df.to_sql()
"""

