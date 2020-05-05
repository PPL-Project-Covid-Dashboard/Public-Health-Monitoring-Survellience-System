import pandas as pd
import numpy as np

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
import datetime

#####################################################################################################################################
# Boostrap CSS and font awesome . Option 1) Run from codepen directly Option 2) Copy css file to assets folder and run locally
#####################################################################################################################################
external_stylesheets = ['https://codepen.io/unicorndy/pen/GRJXrvP.css','https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css']


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Covid19 - Global Dashboard Example'

colors = {
    'background': '#23155c',
    'text': '#56dbdb',
    'figure_text': '#ffffff',
    'confirmed_text':'#f2b56b',
    'deaths_text':'#f44336',
    'recovered_text':'#7ff26b',
    'highest_case_bg':'#393939',
    
}

#Creating custom style for local use
divBorderStyle = {
    'backgroundColor' : '#393939',
    'borderRadius': '12px',
    'lineHeight': 0.9,
}

#Creating custom style for local use
boxBorderStyle = {
    'borderColor' : '#393939',
    'borderStyle': 'solid',
    'borderRadius': '10px',
    'borderWidth':2,
}
# url_confirmed = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
# url_deaths = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
# url_recovered = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'

# Data can also be saved locally and read from local drive
# url_confirmed = 'time_series_covid19_confirmed_global.csv'
# url_deaths = 'time_series_covid19_deaths_global.csv'
# url_recovered = 'time_series_covid19_recovered_global.csv'

# df_confirmed = pd.read_csv(url_confirmed)
# df_deaths = pd.read_csv(url_deaths)
# df_recovered = pd.read_csv(url_recovered)

# print(df_deaths)

# # Total cases
# df_confirmed_total = df_confirmed.iloc[:, 4:].sum(axis=0)
# df_deaths_total = df_deaths.iloc[:, 4:].sum(axis=0)
# df_recovered_total = df_recovered.iloc[:, 4:].sum(axis=0)

# print(type(df_deaths_total))
# print(df_deaths_total)

# df_deaths_confirmed=df_deaths.copy()
# df_deaths_confirmed['confirmed'] = df_confirmed.iloc[:,-1]

# print(type(df_deaths_confirmed))
# print(df_deaths_confirmed)

# #Sorted - df_deaths_confirmed_sorted is different from others, as it is only modified later. Careful of it dataframe structure
# df_deaths_confirmed_sorted = df_deaths_confirmed.sort_values(by=df_deaths_confirmed.columns[-2], ascending=False)[['Country/Region',df_deaths_confirmed.columns[-2],df_deaths_confirmed.columns[-1]]]
# df_recovered_sorted = df_recovered.sort_values(by=df_recovered.columns[-1], ascending=False)[['Country/Region',df_recovered.columns[-1]]]
# df_confirmed_sorted = df_confirmed.sort_values(by=df_confirmed.columns[-1], ascending=False)[['Country/Region',df_confirmed.columns[-1]]]

# #Single day increase
# df_deaths_confirmed_sorted['24hr'] = df_deaths_confirmed_sorted.iloc[:,-2] - df_deaths.sort_values(by=df_deaths.columns[-1], ascending=False)[df_deaths.columns[-2]]
# df_recovered_sorted['24hr'] = df_recovered_sorted.iloc[:,-1] - df_recovered.sort_values(by=df_recovered.columns[-1], ascending=False)[df_recovered.columns[-2]]
# df_confirmed_sorted['24hr'] = df_confirmed_sorted.iloc[:,-1] - df_confirmed.sort_values(by=df_confirmed.columns[-1], ascending=False)[df_confirmed.columns[-2]]

url_confirmed = 'https://api.covid19india.org/csv/latest/state_wise.csv'
#print(url_confirmed)

df_confirmed = pd.read_csv(url_confirmed)
df_deaths = pd.read_csv(url_confirmed)
df_recovered = pd.read_csv(url_confirmed)

# print(df_deaths)
# print(df_confirmed)
# print(type(df_confirmed))

#print(df_confirmed)
df_confirmed_total = df_confirmed.iloc[0]
# print(df_confirmed_total)
df_deaths_total = df_deaths.iloc[0]
# print(df_deaths_total)
df_recovered_total = df_recovered.iloc[0]


app.layout = html.Div(
    html.Div([
         # Header display
        html.Div(
            [
                html.H1(children='Covid-19 (Coronavirus) Interactive Outbreak Tracker',
                        style={
                             'textAlign': 'center',
                             'color': colors['text'],
                             'backgroundColor': colors['background'],
                             'fontFamily':'Bitter-Bold',
                             'fontSize':'50px',
                        },
                        className='ten columns',
                        ),
                html.Div([
                    html.Button(html.I(className="fa fa-info-circle"),
                        id='info-button',
                        style={
                              'color': '#ffffff',
                              'fontSize':'36px'
                        },)
                ],className='two columns',),
                html.Div(children='Best viewed on Desktop. Refresh browser for latest update.',
                         style={
                             'textAlign': 'left',
                             'color': colors['text'],
                             'backgroundColor': colors['background'],
                             'textAlign': 'center',
                             'fontSize':'20px'
                         },
                         className='twelve columns'
                         )
            ], className="row"
        ),

        html.Div([
            html.Div(
                [
                html.H4(children='Total Cases: ',
                       style={
                           'textAlign': 'center',
                           'color': colors['confirmed_text'],
                           'backgroundColor': colors['background'],
                           'marginBottom':'0',
                       }
                       ),
                html.P(f"{df_confirmed_total[1]:,d}",
                       style={
                    'textAlign': 'center',
                    'color': colors['confirmed_text'],
                    'backgroundColor': colors['background'],
                    'fontSize': 30,
                }
                ),
                # html.P('Past 24hrs increase: +' + f"{df_confirmed_total[-1] - df_confirmed_total[-2]:,d}"
                #        + ' (' + str(round(((df_confirmed_total[-1] - df_confirmed_total[-2])/df_confirmed_total[-1])*100, 2)) + '%)',
                #        style={
                #     'textAlign': 'center',
                #     'color': colors['confirmed_text'],
                # }
                # ),
            ],
                style=divBorderStyle,
                className='four columns',
            ),
            html.Div([
                html.H4(children='Total Deceased: ',
                       style={
                           'textAlign': 'center',
                           'color': colors['deaths_text'],
                           'backgroundColor': colors['background'],
                           'marginBottom':'0',
                       }
                       ),
                html.P(f"{df_deaths_total[2]:,d}",
                       style={
                    'textAlign': 'center',
                    'color': colors['deaths_text'],
                    'fontSize': 30,
                    'backgroundColor': colors['background'],
                }
                ),
                # html.P('Mortality Rate: ' + str(round(df_deaths_total[-1]/df_confirmed_total[-1] * 100, 3)) + '%',
                #        style={
                #     'textAlign': 'center',
                #     'color': colors['deaths_text'],
                # }
                # ),
            ],
                style=divBorderStyle,
                className='four columns'),
            html.Div([
                html.H4(children='Total Recovered: ',
                       style={
                           'textAlign': 'center',
                           'color': colors['recovered_text'],
                           'backgroundColor': colors['background'],
                           'marginBottom':'0',
                       }
                       ),
                html.P(f"{df_recovered_total[3]:,d}",
                       style={
                    'textAlign': 'center',
                    'color': colors['recovered_text'],
                    'backgroundColor': colors['background'],
                    'fontSize': 30,
                }
                ),
                # html.P('Recovery Rate: ' + str(round(df_recovered_total[-1]/df_confirmed_total[-1] * 100, 3)) + '%',
                #        style={
                #     'textAlign': 'center',
                #     'color': colors['recovered_text'],
                # }
                # ),
            ],
                style=divBorderStyle,
                className='four columns'),
        ], className='row'),
    ],
        className='ten columns offset-by-one'
    ),
    style={
         'textAlign': 'left',
         'color': colors['text'],
         'backgroundColor': colors['background'],
    },
)


if __name__ == '__main__':
    app.run_server(debug=True)