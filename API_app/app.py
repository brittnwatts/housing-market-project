# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine, func

from flask import Flask, jsonify, request



#################################################
# Database Setup
#################################################
app = Flask(__name__)
engine = create_engine("sqlite:///hv_rc_db.db")


# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
t1 = Base.classes.table1
t2 = Base.classes.table2
t3 = Base.classes.table3
t4 = Base.classes.table4
# Create our session (link) from Python to the DB
# session = Session(engine)
# Need scoped session for ease of use, allows user to run multiple calls in a session
Session = scoped_session(sessionmaker(bind=engine))


#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#Homepage
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"The follwoing route takes input from the user, where City_ST can be replaced with a US city<br/>"
        f"and state (state abbreviated). JSON format is returned for the maximum and minimum home values & date.<br/>"
        f"<br/>"
        f"/analyze_hv?column_name=City_ST<br/>"
        f"Try: /analyze_hv?column_name=Dallas_TX for Dallas, Texas.<br/>"
        f"<br/>"
        f"The follwoing route takes input from the user, where City_ST can be replaced with a US city<br/>"
        f"and state (state abbreviated). JSON format is returned for the maximum and minimum rental costs & date.<br/>"
        f"<br/>"
        f"/analyze_rc?column_name=City_ST<br/>"
        f"Try: /analyze_rc?column_name=Dallas_TX for Dallas, Texas.<br/>"
        f"<br/>"
    )

@app.route('/analyze_hv', methods=['GET'])
def analyze_hv_col():
    # Get the requested column name from the route
    column_name = request.args.get('column_name')

    # Check if the requested column exists in t1, 
    if not hasattr(t1, column_name):
        return jsonify({'error': f'Column {column_name} does not exist in table t1.'})
    
    # Create a new session
    session = Session()

    # Get max & min
    min_value = Session.query(func.min(getattr(t1, column_name))).scalar()
    max_value = Session.query(func.max(getattr(t1, column_name))).scalar()

    # Query the dates for max & min
    min_date = Session.query(t1.Date).filter(getattr(t1, column_name) == min_value).scalar()
    max_date = Session.query(t1.Date).filter(getattr(t1, column_name) == max_value).scalar()

    # Prepare dictionary
    analysis_result = {
        'column_name': column_name,
        'min_value': min_value,
        'min_date': min_date,
        'max_value': max_value,
        'max_date': max_date,
    }

    return jsonify(analysis_result)
    session.close()

@app.route('/analyze_rc', methods=['GET'])
def analyze_rc_col():
    # Get the requested column name from the route
    column_name = request.args.get('column_name')

    # Check if the requested column exists in t2
    if not hasattr(t2, column_name):
        return jsonify({'error': f'Column {column_name} does not exist in table t2.'})
    
    # Create a new session
    session = Session()
    

    # Get max & min
    min_value = Session.query(func.min(getattr(t2, column_name))).scalar()
    max_value = Session.query(func.max(getattr(t2, column_name))).scalar()

    # Query the dates for max & min
    min_date = Session.query(t2.Date).filter(getattr(t2, column_name) == min_value).scalar()
    max_date = Session.query(t2.Date).filter(getattr(t2, column_name) == max_value).scalar()

    # Prepare dict.
    rc_min_max = {
        'column_name': column_name,
        'min_value': min_value,
        'min_date': min_date,
        'max_value': max_value,
        'max_date': max_date,
    }

    return jsonify(rc_min_max)
    session.close()

if __name__ == '__main__':
    app.run(debug=True)

