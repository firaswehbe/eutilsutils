#!/usr/bin/env python

#######################################
# DB Setup
# Use this to create engine, session, and Base

import sqlalchemy as SA
import sqlalchemy.orm as SAORM

#should use proper config module or something
myengineurl = 'postgresql://eutilsutils_user:xxx@localhost:5432/eutilsutils_db'
myengine = SA.create_engine(myengineurl)
# look into scoped_session
mysession = SAORM.sessionmaker(myengine)
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
# Do the thing

Base.metadata.create_all(bind=myengine)
