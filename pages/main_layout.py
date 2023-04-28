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
# Space components
space = dbc.Row("  ", style={"height": "10px"})
# Mini space
miniSpace = dbc.Row("  ", style={"height": "5px"})
# Cards shadow
cardShadow = ["shadow-sm p-3 mb-5 bg-white rounded", {"margin-top": "-2em"}]
class mainLayout(object):
    def __init__(self):
        pass
    
    def define_main_page(self, Lab_df = False):
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
                                        # dbc.Col(space),
                                        dbc.Col(self.define_duration_card()),
                                        dbc.Col(self.define_lab_control(Lab_df = Lab_df)),
                                        # dbc.Col(Analyzer_control,),
                                        # dbc.Col(Test_control),
                                        # dbc.Col(QC),
                                        # dbc.Col(plotButton),
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
                                            # dbc.Card([
                                            # dbc.Col(space),
                                            # #dbc.Col(creat_calc_table(graph_calcs)),
                                            # dbc.Col(space),
                                            # dcc.Graph(id="cluster-graph",)
                                            # ]),
                                            id="graph_container"),
                                            html.Hr(
                                            # style={"margin-top": "-1em"}
                                            ),
                                            # dbc.Row([
                                            #     dbc.Col(DrawCalcMeanOption()
                                            #     ,md=4, style= {"text-align": "center"}
                                            #     ),
                                            #     dbc.Col(
                                            #         Graph_Rules
                                            #     ,md=4, style= {"text-align": "center"}
                                            #     ),
                                            # ])
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

    def define_lab_control(self, Lab_df = False):
        # Card to select Lab branch and unit of the data
        Lab_control = dbc.Card(
            [
                dbc.FormGroup(
                    [
                    dbc.Label('Lab'),
                    dbc.Col(space),
                    dcc.Dropdown(
                        id='Lab_branch',
                        options=[
                            {'label':name, 'value':name} for name in Lab_df.lab_branch],
                        placeholder = 'Select Branch'
                    ),
                    dbc.Col(space),
                    dcc.Dropdown(
                        id='Lab_unit',
                        disabled = True,
                        placeholder = 'Select Unit'
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
    
    
    
    