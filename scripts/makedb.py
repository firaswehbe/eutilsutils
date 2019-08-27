#!/usr/bin/env python

import sqlalchemy as SA
import configparser

myconfig = configparser.ConfigParser()
myconfig.read('../config/config.ini')

myenginestr = 'postgres://{0}:{1}@{2}:{3}/{4}'.format(
        myconfig.get('database','dbuser',fallback=''),
        myconfig.get('database','dbpassword',fallback=''),
        myconfig.get('database','dbhost',fallback=''),
        myconfig.get('database','dbport',fallback=''),
        myconfig.get('database','dbname',fallback='')
        )
        

myengine = SA.create_engine(myenginestr)

mymetadata = SA.MetaData()

eusummaries = SA.Table('esummaries', mymetadata,
    SA.Column('pmid', SA.Integer, primary_key=True),
    SA.Column('authors', SA.String),
    SA.Column('title', SA.String),
    SA.Column('source', SA.String),
    SA.Column('so', SA.String)
)

mymetadata.create_all(myengine)
