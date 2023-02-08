# Using flask to make an api
# import necessary libraries and functions
from pickle import TRUE
from sre_constants import SUCCESS
from flask import Flask, jsonify, render_template, request
from flask_swagger_ui import get_swaggerui_blueprint
import sqlite3
  
# creating a Flask app
app = Flask(__name__)

### swagger specific ###
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Seans-Python-Flask-REST-Boilerplate"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

app.register_blueprint(swaggerui_blueprint)
                        
def responde_with(data, success = True, message = "SUCCESS"):
    response =  jsonify({
        "success": success,
        "data": data,
        "message": message
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
  
    return response

@app.route('/api/weather/stats/', methods = ['GET'])
def get_stats():
    with sqlite3.connect('./test.db') as db:
        db.row_factory = sqlite3.Row  
        arguments = request.args
        where_clauses = []
        if 'year' in arguments:
        	date_param = arguments["year"]
        	where_clauses.append(f"year='{date_param}'")
        if 'station' in arguments:
        	station = arguments["station"]
        	where_clauses.append(f"region='{station}'")
        where_clause = ""
        if len(where_clauses):
        	where_clause =" where " + " and ".join(where_clauses)
        
        cursor_obj = db.cursor()
        cursor_obj.execute(f'SELECT * FROM WEATHER_DATA_MATRICS {where_clause}')
        data = cursor_obj.fetchall()
        data = [ list(row) for row in data ]
        return responde_with(data);

@app.route('/api/weather/', methods = ['GET'])
def get_weather():
    with sqlite3.connect('./test.db') as db:
        db.row_factory = sqlite3.Row  
        arguments = request.args
        where_clauses = []
        if 'date' in arguments:
        	date_param = arguments["date"]
        	where_clauses.append(f"record_date='{date_param}'")
        if 'station' in arguments:
        	station = arguments["station"]
        	where_clauses.append(f"region='{station}'")
        where_clause = ""
        if len(where_clauses):
        	where_clause =" where " + " and ".join(where_clauses)
        
        cursor_obj = db.cursor()
        cursor_obj.execute(f'SELECT * FROM WEATHER_DATA {where_clause}')
        data = cursor_obj.fetchall()
        data = [ list(row) for row in data ]
        return responde_with(data);


    

# driver function
if __name__ == '__main__':
  
    app.run(debug = True)