# Generally follows the flow of a Flask app had we made a create_app method 
# to initialize everythin. doing it in the constructor of the class here

import configparser
from Bio import Entrez
from eutilsutils.database import EutilsUtilsDB
import os

class EutilsUtils:
    def __init__(self, rootlocation: str = None, configlocation: str = None):
        # In Flask, root and config file location can be automatically inferred
        # Need to insert some checks that it is a valid and accessible path
        # Ditto for config location
        if rootlocation is None:
            rootlocation = os.getcwd()
        
        if configlocation is None:
            configlocation = os.path.join(rootlocation,'config/config.ini')

        self.root = rootlocation

        self.config = configparser.ConfigParser()
        self.config.read(configlocation)

        self.db = EutilsUtilsDB(self.config)

        # Not sure if you can embed an entire module name space to an object attribute
        self.en = Entrez
        self.en.email = self.config['pubmed']['email']
        self.en.api_key = self.config['pubmed']['api_key']
