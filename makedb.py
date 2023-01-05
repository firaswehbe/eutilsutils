#!/usr/bin/env python

from eutilsutils import EutilsUtils
from eutilsutils.model import EutilsUtilsBaseModel
import argparse
import rich.console
import sys
import sqlalchemy as SA

if __name__!='__main__': raise ImportError("makedb.py is not intended as a module")

myargparser = argparse.ArgumentParser(description="Utility script to initialize or drop the database")
mygroup1 = myargparser.add_mutually_exclusive_group()
mygroup1.add_argument("-d","--drop",help="Drop DB first",action="store_true")
mygroup1.add_argument("-o","--overwrite",help="Don't drop entire DB but can overwrite existing files",action="store_true")
myargs = myargparser.parse_args()

myconsole = rich.console.Console(style='green on black')
app = EutilsUtils()

myconsole.print("Successfully create an EutilsUtils app object")
myconsole.print(f"Root directory: [bright_white]{app.rootlocation}")
myconsole.print(f"Config location: [bright_white]{app.configlocation}")

myconsole.print("[bright_white]EutilsUtils[/bright_white] model tables:")
for myeutilsutilstable in EutilsUtilsBaseModel.metadata.sorted_tables:
    myconsole.print(f"\t[bright_white]{myeutilsutilstable}")

myconsole.print(f"[bright_white]Existing[/bright_white] tables in the database ([bright_yellow]yellow[/bright_yellow] tables are in the model)")
myexistingmetadata = SA.MetaData()
myexistingmetadata.reflect(bind=app.db.engine)
for myexistingtable in myexistingmetadata.sorted_tables:
    mycolor = 'bright_yellow' if str(myexistingtable) in EutilsUtilsBaseModel.metadata.tables else 'bright_white'
    myconsole.print(f"\t[{mycolor}]{myexistingtable}")

myconsole.print("Model tables not in the database will be created.")
if myargs.overwrite:
    myconsole.print("[bright_yellow]The yellow tables will be overwritten.[/bright_yellow]")
elif myargs.drop: 
    myconsole.print("[bright_red]ALL TABLES IN THE DATABASE WILL BE DROPPED FIRST[/bright_red]")

myconfirmation = myconsole.input('Are you sure you want to continue? (yes/\[no]) ')
if myconfirmation!='yes':
    sys.exit()

if myargs.overwrite:
    EutilsUtilsBaseModel.metadata.drop_all(bind=app.db.engine) 
    EutilsUtilsBaseModel.metadata.create_all(bind=app.db.engine)
elif myargs.drop: 
    myexistingmetadata.drop_all(bind=app.db.engine) 
    EutilsUtilsBaseModel.metadata.create_all(bind=app.db.engine)
else:
    EutilsUtilsBaseModel.metadata.create_all(bind=app.db.engine)

myconsole.print("Creating new tables")

myexistingmetadata = SA.MetaData()
myexistingmetadata.reflect(bind=app.db.engine)
for myexistingtable in myexistingmetadata.sorted_tables:
    mycolor = 'bright_yellow' if str(myexistingtable) in EutilsUtilsBaseModel.metadata.tables else 'bright_white'
    myconsole.print(f"\t[{mycolor}]{myexistingtable}")