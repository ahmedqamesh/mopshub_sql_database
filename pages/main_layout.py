from __future__ import division
import logging
import os
import yaml
import tables as tb
import numpy as np
import pandas as pd
import csv
from pathlib import Path
import coloredlogs as cl
import socket
import ipaddress
from dash import Dash, html, dcc, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash_bootstrap_components import themes
from dash_bootstrap_components._components.Button import Button
from dash_bootstrap_components._components.Col import Col
from dash_bootstrap_components._components.NavItem import NavItem
from dash_bootstrap_components._components.Row import Row
from sklearn import datasets
from sqlAnalysis.analysis_utils  import AnalysisUtils
from sqlAnalysis.analysis  import Analysis

# Space components
space = dbc.Row("  ", style={"height": "10px"})
# Mini space
miniSpace = dbc.Row("  ", style={"height": "5px"})
# Cards shadow
cardShadow = ["shadow-sm p-3 mb-5 bg-white rounded", {"margin-top": "-2em"}]
class mainLayout(object):
    def __init__(self, mydb = False):
        iris_raw = datasets.load_iris()
        self.iris = pd.DataFrame(iris_raw["data"], columns=iris_raw["feature_names"])
        self.patch_panel_df = self.sql_dash_interface(sql_database = mydb, table_query = "patch_panel", sql_table = "patch_panels") 
        self.hw_unit_df = self.sql_dash_interface(sql_database = mydb, table_query = "hw_unit", sql_table = "patch_panels") 
        self.QC_df = self.sql_dash_interface(sql_database = mydb, table_query = "qc_lot_number,qc_name", sql_table = "QC_Parameters") 
        #pass

    def create_graph_calcs(self):
        # Array of table attributes
        # tableCols = ['Mean', 'SD', 'CV', 'MU measurments', 'EWMA',
        #              'CUSUM', 'Target Mean', 'Actual Mean', 'Target SD', 'Actual SD']
        Mean_Table_cols = ['Assigned Mean','Caculated Mean', 'Assigned SD',  'Calculated SD']
        CV_Table_cols = ['CV %', 'MU Measurments']
        # tableCols = [Analyzer_df.analyzer_name[0],Analyzer_df.analyzer_name[1], Analyzer_df.analyzer_name[2]]
        
        # Array of table values
        Mean_Table_values = [0,0,0,0]
        CV_Table_values = [0,0]

        # Array of table rows
        Mean_Table_Data = [
            html.Tr([html.Td(Mean_Table_cols[0],className="table-active"),html.Td(Mean_Table_values[0]),html.Td(Mean_Table_cols[1],className="table-active"),html.Td(Mean_Table_values[1])]), 
            html.Tr([html.Td(Mean_Table_cols[2],className="table-active"),html.Td(Mean_Table_values[2]),html.Td(Mean_Table_cols[3],className="table-active"),html.Td(Mean_Table_values[3])])
        ]

        CV_Table_Data = [
            html.Tr([html.Td(CV_Table_cols[0],className="table-active"),html.Td(CV_Table_values[0])]), 
            html.Tr([html.Td(CV_Table_cols[1],className="table-active"),html.Td(CV_Table_values[1])])
        ]
        
        graph_calcs=[
                        html.Tr( [html.Th('Assigned Mean'), html.Th(Mean_Table_values[0],style={'font-weight':'normal','border-right':'1px solid #B3B6B7'}),html.Th("Calculated Mean"), html.Th(Mean_Table_values[1],style={'font-weight':'normal'})], style={'font-size':'small','border-bottom':'1px solid #B3B6B7'} ),
                        html.Tr( [html.Td('Assigned SD',style={'font-weight':'bold'}),html.Td(Mean_Table_values[2],style={'border-right':'1px solid #B3B6B7'}),html.Td('Calculated SD',style={'font-weight':'bold'}),html.Td(Mean_Table_values[3])]),
                        
                    ]
        
        return graph_calcs

    def Updata_Calcs_Table_Data(self, MeanTableValuesArray,CVTableValuesArray):
        graph_calcs=[
                    html.Tr( [html.Th('Assigned Mean'), html.Th(Mean_Table_values[0],style={'font-weight':'normal','border-right':'1px solid #B3B6B7'}),html.Th("Calculated Mean"), html.Th(Mean_Table_values[1],style={'font-weight':'normal'})], style={'font-size':'small','border-bottom':'1px solid #B3B6B7'} ),
                    html.Tr( [html.Td('Assigned SD',style={'font-weight':'bold'}),html.Td(Mean_Table_values[2],style={'border-right':'1px solid #B3B6B7'}),html.Td('Calculated SD',style={'font-weight':'bold'}),html.Td(Mean_Table_values[3])]),
                    
                ]
        Mean_Table_Data = [
        html.Tr([html.Td(Mean_Table_cols[0],className="table-active"),html.Td(Mean_Table_values[0]),html.Td(Mean_Table_cols[1],className="table-active"),html.Td(MeanTableValuesArray[1])]), 
        html.Tr([html.Td(Mean_Table_cols[2],className="table-active"),html.Td(Mean_Table_values[2]),html.Td(Mean_Table_cols[3],className="table-active"),html.Td(MeanTableValuesArray[3])])
        ]
        CV_Table_Data = [
        html.Tr([html.Td(CV_Table_cols[0],className="table-active"),html.Td(CVTableValuesArray[0])]), 
        html.Tr([html.Td(CV_Table_cols[1],className="table-active"),html.Td(CVTableValuesArray[1])])
    ]    
        return graph_calcs,CV_Table_Data

    
    def sql_dash_interface(self, sql_database = None, table_query = None, sql_table = None):
        # Read SQL query or database table into a DataFrame.
        data_frame = pd.read_sql(f"SELECT DISTINCT {table_query} FROM {sql_table} ", sql_database)        
        return data_frame    

    def DrawCalcMeanOption(self):
        # ID = 'Draw_calc_Mean_option' + str(i)
        # print (ID)
        DrawCalcMeanOption = html.Div([
        
            dbc.Label('Calculated Mean Line'),
            dcc.RadioItems(
                        id='Draw_calc_Mean_option0',
                        options=[{'label': i, 'value': i} for i in ['Show', 'Hide']],
                        value='Hide',
                        labelStyle={'display': 'block',"text-align": "center"}
                    )
        ])
        return DrawCalcMeanOption
    
    def define_main_page(self, patch_panel_df = False):

        # Calculate Statistical calculations and plot control chart
        plotButton = dbc.Button("Calculate and Plot", 
                                id='Plot_Button',n_clicks = 0, outline=True, color='secondary', block=True,
                                style={'background-color': '#2D4D61 !important',
                                       "margin-top": "-1em"}
                                )
        Graph_Rules = [dbc.Label('Choose Graph Rule'),
                        dcc.Checklist(
                        id = 'Graph_Rules',
                        options=[
                            {'label': ' 1-2S', 'value': '1-2S'},
                            {'label': ' 1-3S', 'value': '1-3S'},
                            {'label': ' 2-2S', 'value': '2-2S'},
                            {'label': ' 4-1S', 'value': '4-1S'},
                            {'label': ' n-XS', 'value': 'n-XS'},
                        ],
                        value=['1-2S', '1-3S'],
                        labelStyle={'display': 'block'}
                    )]

        main_page = dbc.Container(
                [
                    dbc.Row(dbc.Col(self.define_navigation_bar(), md=12)),
                    dbc.Row(
                        [
                            # Filters card
                            dbc.Col([
                                dbc.Card(
                                    [    
                                        # dcc.Store(id ='myresult_analyzer_memory'),
                                        # dcc.Store(id='myresult_test_memory'),
                                        # dcc.Store(id='myresult_qc_lot_num_memory'),
                                        # dcc.Store(id='myresult_qc_name_memory'),     
                                        # dcc.Store(id='myresult_qc_level_memory'),
                                        # dcc.Store(id='myresult_qc_Duration_memory'),                                                       
                                        dbc.Col(space),
                                        dbc.Col(self.define_duration_card()),
                                        dbc.Col(self.define_lab_control()),
                                        dbc.Col(self.define_analyzer_control()),
                                        dbc.Col(self.define_test_control()),
                                        dbc.Col(self.define_quality_control()),
                                        dbc.Col(plotButton),
                                        dcc.ConfirmDialog(
                                        id='error-message',
                                        displayed=False,
                                        message='Data Not Found'
                                        ), 
                                       dbc.Col(space)
                                    ],
                                    body=True,
                                    style={'height': '150 vmax', "overflowY": "scroll"}
                                    # className = "shadow-sm p-3 mb-5 bg-white rounded"
                                    
                                )
                            ], md=4, style={'height':'fixed'}),
            
                            # Calculations and plot card
                            dbc.Col([
                               dbc.Col(space),
                                dbc.Card(
                                        [
                                            html.Div(
                                            dbc.Card([
                                            dbc.Col(space),
                                            dbc.Col(self.create_calc_table(self.create_graph_calcs())),
                                            dbc.Col(space),
                                            dcc.Graph(id="cluster-graph",)
                                             ]),
                                            id="graph_container"),
                                            html.Hr(
                                            # style={"margin-top": "-1em"}
                                            ),
                                            dbc.Row([
                                                dbc.Col(self.DrawCalcMeanOption()
                                                ,md=4, style= {"text-align": "center"}
                                                ),
                                                dbc.Col(
                                                    Graph_Rules
                                                ,md=4, style= {"text-align": "center"}
                                                ),
                                            ])
                                        ],
                                        id='initial_graph',
                                        body=True,
                                        className="shadow-sm p-3 mb-5 bg-white rounded",
                                        style={"margin-top": "-0.5em"}
                                    ),
            
                            ], md=8, style={'width':'100%'}),
                        ],
                        align="top",
                        style={"margin-top": "1rem", "padding-bottom": "1rem"}
                    ),
                ],
                style={"background-color": "#eaeaea", "height": "100%", "position": 'flex'},
                # className = "container-xl",
                fluid=True,
            
            )        
        return main_page


    def DrawCalcMeanOption(self):
        # ID = 'Draw_calc_Mean_option' + str(i)
        # print (ID)
        DrawCalcMeanOption = html.Div([
        
            dbc.Label('Calculated Mean Line'),
            dcc.RadioItems(
                        id='Draw_calc_Mean_option0',
                        options=[{'label': i, 'value': i} for i in ['Show', 'Hide']],
                        value='Hide',
                        labelStyle={'display': 'block',"text-align": "center"}
                    )
        ])
        return DrawCalcMeanOption
    

    def define_analyzer_control(self):
        # Card to select Analyzer name and code of the data
        Analyzer_control = dbc.Card(
            [
                dbc.FormGroup(
                    [
                    dbc.Label('Analyzer'),
                    dbc.Col(space),
                    dcc.Dropdown(
                        id='Analyzer_Name',
                        disabled = True,
                        placeholder = 'Select Analyzer Name'
                    ),
                    ],
                ),
            ],
            body=True,
            className=cardShadow[0],
            style=cardShadow[1]
        )


    def define_test_control(self):
        # Card to select Test code , name and reagent lot number
        Test_control = dbc.Card(
            [
                dbc.FormGroup(
                    [
                        dbc.Label('Test'),
                        dcc.Dropdown(
                            id='Test_Name',
                            disabled = True,
                            placeholder='Select Test Name'
                        ),
                        
                        # dbc.Col(space),
                        # dcc.Dropdown(
                        #     id='Reagent_Num',
                        #     value="Reagent_Num",
                        #     multi=True,
                        #     placeholder='Select Reagent Lot Number',
                        #     disabled = True
                        # ),
                    ],
                )
            ],
            body=True,
            className=cardShadow[0],
            style=cardShadow[1]
        )



    def define_quality_control(self):
        # Card to select quality control name and level
        QC = dbc.Card(
            [
                dbc.FormGroup(
                    [
                        dbc.Label('QC'),
                        dcc.Dropdown(
                            id='QC_Num',
                            options=[
                                {"label": col, "value": col}for col in self.QC_df.qc_lot_number],
                            placeholder='Select QC Lot Number',
                            disabled = True
        
                        ),
                        dbc.Col(space),
                        dcc.Dropdown(
                            id='QC_Name',
                            options=[
                                {"label": col, "value": col}for col in self.QC_df.qc_name],
                            disabled = True,
                            placeholder='Select QC Name'
                        ),
                        dbc.Col(space),
                        dcc.Dropdown(
                            id='QC_Level',
                            options=[
                                {"label": col, "value": col}for col in self.iris.columns],
                            multi=True,
                            disabled = True,
                            placeholder='Select QC Level'
                        ),
                    ],
                )
            ],
            body=True,
            className=cardShadow[0],
            style=cardShadow[1]
        )

# Create Table of calculations
    def create_calc_table(self, graph_calcs = None):
        Calculations = dbc.Card([
                                dbc.Col(space),
                                dbc.Table(html.Tbody(graph_calcs),  id='Mean_Table',borderless = True,responsive = True, size = 'sm',
                                style = {'font-size':'small','width':'50%','margin-left':'15px'} )
                                ])
        return Calculations

    def define_lab_control(self):
        # Card to select Lab branch and unit of the data
        Lab_control = dbc.Card(
            [
                dbc.FormGroup(
                    [
                    dbc.Label('Patch Panel'),
                    dbc.Col(space),
                    dcc.Dropdown(
                        id='patch_panel',
                        options=[
                            {'label':name, 'value':name} for name in self.patch_panel_df.patch_panel],
                        placeholder = 'Select Patch Panel'
                    ),
                    dbc.Col(space),
                    dcc.Dropdown(
                        id='hw_unit',
                        disabled = False,
                        options=[
                            {'label':name, 'value':name} for name in self.hw_unit_df.hw_unit],
                        placeholder = 'Select Hardware unit'
                    ),
                    ],
                ),
            ],
            body=True,
            className=cardShadow[0],
            style=cardShadow[1]
        )
        return Lab_control
    
    def define_duration_card(self):

        
        # Mini space
        miniSpace = dbc.Row("  ", style={"height": "5px"})
        
        # Cards shadow
        cardShadow = ["shadow-sm p-3 mb-5 bg-white rounded", {"margin-top": "-2em"}]
        
        # Card to select period of time for data to plot it
        duration = dbc.Card(
            [
                dbc.FormGroup(
                    [
                        dbc.Col([
                            dbc.Label('Priod Of Time'),
                            dbc.Col(miniSpace),
                            dcc.DatePickerRange(
                                id='my-date-picker-range',
                                start_date_placeholder_text="Start Period",
                                end_date_placeholder_text="End Period",
                                calendar_orientation='vertical'
                            ),
                            dbc.Col(space),
                            html.Div(id='output-container-date-picker-range',)
                        ]),
                    ], row=True,
                ),
            ],
            body=True,
            className=cardShadow[0],
        )
        return duration

    def define_navigation_bar(self):
        # --------------------------------------------------------------Nav Bar---------------------------------------
        # App Logo image
        Logo = "https://icon-library.com/images/graphs-icon/graphs-icon-4.jpg"
        # make a reuseable navitem for the different examples
        nav_item = dbc.NavItem(dbc.NavLink(
            'Home', href="#", style={"color": "#caccce"},))
        nav_item2 = dbc.NavItem(dbc.NavLink(
            'Results', href="#", style={"color": "#caccce"},))
        # make a reuseable dropdown for the different examples
        dropdown = dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem(
                    "more pages", header=True),
                dbc.DropdownMenuItem(
                    "Add QC", href="#", style={'color': '#caccce', 'hover': {'color': '#2e4d61'}})
            ],
            nav=True,
            in_navbar=True,
            label="Menu",
        ) 
        NavBar = dbc.Navbar(
            dbc.Container(
                [
                    html.A(
                        # Use row and col to control vertical alignment of logo / brand
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=Logo, height="50px")),
                                dbc.Col(dbc.NavbarBrand(html.H4("MOPS-HUB database", className="ml-2",
                                style={'font-weight': 'bold', 'color': '#caccce', }))),
                            ],
                            align="center",
                            no_gutters=True,
                        ),
                        href="#",
                    ),
                    dbc.NavbarToggler(id="navbar-toggler2", n_clicks=0),
                    dbc.Collapse(
                        dbc.Nav(
                            [nav_item, nav_item2, dropdown], className="ml-auto", navbar=True
                        ),
                        id="navbar-collapse2",
                        navbar=True,
                    ),
                ],
                fluid=True,
            ),
            color="#2e4d61",
            dark=True,
            className="mb-10",
        )        
        return NavBar
