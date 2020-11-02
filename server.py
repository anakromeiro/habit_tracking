from flask import (Flask, request, render_template)
from flask_restful import Resource, Api
# local modules
import config

# Get the application instance
connex_app = config.connex_app

# Read the swagger.yml file to configure the endpoints
connex_app.add_api("swagger.yml")

# create a URL route in our application for "/"
@connex_app.route("/")
def home():
    """
    This function just responds to the browser ULR localhost:5000/

    :return: the rendered template 'home.html'
    """    
    
    # having an index.html file in the templates directory causes problems once you import the Connexion module in your program, this is the reason the file is called home.html
    return render_template('home.html')


if __name__ == '__main__':
    connex_app.run(host='0.0.0.0', debug=True)