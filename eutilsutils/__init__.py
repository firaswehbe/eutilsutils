from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return 'There are {0} papers in the database.'.format( 'XX' )
