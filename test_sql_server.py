from os import name, terminal_size
from dash import Dash, html, dcc, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash_bootstrap_components import themes
from dash_bootstrap_components._components.Button import Button
from dash_bootstrap_components._components.Col import Col
from dash_bootstrap_components._components.NavItem import NavItem
from dash_bootstrap_components._components.Row import Row
from datetime import datetime as dt
from datetime import date
import numpy as np
from numpy.core.arrayprint import printoptions
from numpy.core.fromnumeric import size
from numpy.core.numeric import NaN
from numpy.lib.function_base import append
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from sklearn import datasets
import csv
import math
import statistics
from uncertainties import ufloat
import sqlalchemy as sa
from sqlAnalysis.analysis import  Analysis
from sqlAnalysis.analysis_utils import   AnalysisUtils
import mysql.connector
from db import sql_database
from pages.main_layout import mainLayout

# The iris dataset is a classic and very easy multi-class classification dataset.
def sql_dash_interface(sql_database = None):
    iris_raw = datasets.load_iris()
    iris = pd.DataFrame(iris_raw["data"], columns=iris_raw["feature_names"])
    QC_df = pd.read_sql("SELECT qc_lot_number,qc_name FROM QC_Parameters ", sql_database) 

# Read SQL query or database table into a DataFrame.
# Array of table attributes
Mean_Table_cols = ['Assigned Mean', 'Caculated Mean', 'Assigned SD', 'Calculated SD']
CV_Table_cols = ['CV %', 'MU Measurments']

# Array of initial table values
Mean_Table_values = [0, 0, 0, 0]
CV_Table_values = [0, 0]

if __name__ == '__main__':
    database = sql_database.SQLDataBase()
    mydb = database.get_database()
    # Main Application page
    app = Dash('Test SQL', external_stylesheets=[
                    dbc.themes.MINTY, dbc.themes.BOOTSTRAP])
    # Call app cards
    app.layout = mainLayout(mydb = mydb).define_main_page()
    app.run_server(debug=True)
