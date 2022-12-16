import sqlalchemy as SA
import sqlalchemy.orm as SAORM


class EutilsUtilsDB:
    """General utility database class for access to SQL alchemy stuff
    """
    def __init__(self,config_object):
        self.engine = makeEngine(makeEngineURL(config_object))
        # look into scoped_session
        self.session_maker = SAORM.sessionmaker(self.engine)


def makeEngineURL(config_object):
    myuser = config_object['database']['dbuser']
    mypass = config_object['database']['dbpassword']
    myhost = config_object['database']['dbhost']
    myport = config_object['database']['dbport']
    mydb   = config_object['database']['dbname']
    return f"postgresql://{myuser}:{mypass}@{myhost}:{myport}/{mydb}"

def makeEngine(engine_url):
    return SA.create_engine(engine_url)

