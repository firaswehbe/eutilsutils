import flask
import os

def create_app(): 
    app = flask.Flask(__name__,instance_relative_config=True)
    app.logger.info('initiated')

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    try:
        app.config.from_pyfile('application.cfg')
    except:
        app.logger.error('Could not open config file')
        flask.abort(500)


    @app.route('/')
    def home():
        app.logger.info('home')
        return 'There are {0} papers in the database.'.format( 'XX' )

    return app
