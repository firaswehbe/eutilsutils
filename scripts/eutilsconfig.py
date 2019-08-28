if __name__ == '__main__':
    import sys
    sys.exit("This script is not intended to be run directly from command line")

import configparser as _cp

_myconfig = _cp.ConfigParser()
_myconfig.read('../config/config.ini')

myenginestr = 'postgres://{0}:{1}@{2}:{3}/{4}'.format(
        _myconfig.get('database','dbuser',fallback=''),
        _myconfig.get('database','dbpassword',fallback=''),
        _myconfig.get('database','dbhost',fallback=''),
        _myconfig.get('database','dbport',fallback=''),
        _myconfig.get('database','dbname',fallback='')
        )
