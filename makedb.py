#!/usr/bin/env python

# Consider adding argparse for argument and rich output

from eutilsutils import EutilsUtils
from eutilsutils.model import EutilsUtilsBaseModel

app = EutilsUtils()

EutilsUtilsBaseModel.metadata.drop_all(bind=app.db.engine)
EutilsUtilsBaseModel.metadata.create_all(bind=app.db.engine)
