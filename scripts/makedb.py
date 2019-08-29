#!/usr/bin/env python

if __name__ != '__main__':
    import sys
    sys.exit("This script cannot be imported, only run from command line")

import sqlalchemy as SA
import eutilsconfig as EC
import argparse
import logging

myargparser = argparse.ArgumentParser(description='Create empty database for eutilsutils')
myargparser.add_argument("-t", "--tablename", help="The new table you want to create. [NOT IMPLEMENTED]", nargs="*")
myargparser.add_argument("-d", "--drop", help="Drop table(s) if they exist", action="store_true")
myargs = myargparser.parse_args()

logging.basicConfig(filename='log/scripts.log',level=logging.DEBUG,format='%(asctime)s %(levelname)s:%(filename)s:%(lineno)s:%(message)s')

myengine = SA.create_engine(EC.myenginestr)
mymetadata = SA.MetaData()

eusummaries = SA.Table('esummaries', mymetadata,
    SA.Column('pmid', SA.Integer, primary_key=True),
    SA.Column('authors', SA.String),
    SA.Column('title', SA.String),
    SA.Column('source', SA.String),
    SA.Column('so', SA.String)
)

if myargs.drop: 
    mymetadata.drop_all(myengine)
    logging.warning('Dropped all tables in schema:{0}'.format(','.join(mymetadata.tables)))
mymetadata.create_all(myengine)
logging.info('Created tables in schema:{0}'.format(','.join(mymetadata.tables)))
