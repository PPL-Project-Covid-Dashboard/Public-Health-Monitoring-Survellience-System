import pandas as pd
import numpy as np

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

#####################################################################################################################################
# Boostrap CSS and font awesome . Option 1) Run from codepen directly Option 2) Copy css file to assets folder and run locally
#####################################################################################################################################
external_stylesheets = ['https://codepen.io/unicorndy/pen/GRJXrvP.css','https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css', 'styles.css']


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Covid19 - Global Dashboard Example'

colors = {
    'background': '#000000',
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

df_active_total = df_recovered.iloc[0]

#for highest case
df_confirmed_sorted = df_confirmed.iloc[1:, :2]
#df_deaths_sorted = df_deaths.iloc[1:, 0:4:3]
df_recovered_sorted = df_recovered.sort_values(by=df_recovered.columns[2], ascending=False)[['State',df_recovered.columns[2]]]
df_deaths_sorted = df_deaths.sort_values(by=df_deaths.columns[3], ascending=False)[['State',df_confirmed.columns[3]]]

#for past 24 hrs
df_confirmed_sorted_1 = df_confirmed.sort_values(by=df_confirmed.columns[7], ascending = False)[['State', df_confirmed.columns[7]]]
df_recovered_sorted_1 = df_recovered.sort_values(by=df_recovered.columns[7], ascending = False)[['State', df_recovered.columns[7]]]
df_deaths_sorted_1 = df_deaths.sort_values(by=df_deaths.columns[7], ascending = False)[['State', df_deaths.columns[7]]]

#for displaying highest count states
df_confirmed_sorted_1 = df_confirmed_sorted_1.iloc[1:, :]



def high_cases(state,total):
    return html.P([ html.Span(state + ' | ' + f"{int(total):,d}",
                        style={'backgroundColor': colors['highest_case_bg'], 'borderRadius': '6px', 'color':'#d7b5f7',}),

            ]
        )


noToDisplay = 8

confirm_cases = []
for i in range(noToDisplay):
    confirm_cases.append(high_cases(df_confirmed_sorted.iloc[i,0],df_confirmed_sorted.iloc[i,1]))


deaths_cases = []
for i in range(noToDisplay):
    deaths_cases.append(high_cases(df_deaths_sorted.iloc[i+1,0],df_deaths_sorted.iloc[i+1,1]))


url_states = pd.read_csv('states.txt')
#print(url_states)

# Recreate required columns for map data
map_data = df_confirmed[["State"]]
map_data = map_data.iloc[1:]
map_data['Latitude'] = url_states.loc[:, url_states.columns[1]]
map_data['Longitude'] = url_states.loc[:, url_states.columns[2]]
#print(map_data)


map_data['Confirmed'] = df_confirmed.loc[1:, df_confirmed.columns[1]]
map_data['Deaths'] = df_deaths.loc[:, df_deaths.columns[3]]
map_data['Recovered'] = df_recovered.loc[:, df_recovered.columns[2]]

#last 24 hours increase
map_data['Deaths_24hr']=df_deaths_sorted_1.iloc[1:,1]
map_data['Recovered_24hr']=df_recovered_sorted_1.iloc[1:,1]
map_data['Confirmed_24hr']=df_confirmed_sorted_1.iloc[1:,1]
map_data.sort_values(by='Confirmed', ascending=False,inplace=True)


#############################################################################
# mapbox_access_token keys, not all mapbox function require token to function.
#############################################################################
mapbox_access_token = 'pk.eyJ1IjoiMTExODAzMTU3IiwiYSI6ImNrOWliY3kzZDAwM2wzbHBqOHhqbnBwcHcifQ.hCWC05VqD38sJxDYlHGR8Q'

####################################################
# Prepare plotly figure to attached to dcc component
# Global outbreak Plot
####################################################
# Change date index to datetimeindex and share x-axis with all the plot
def draw_global_graph(df_confirmed_total,df_deaths_total,df_recovered_total,graph_type='Total Cases'):
    df_confirmed_total.index = pd.to_datetime(df_confirmed_total.index)

    if graph_type == 'Daily Cases':
        df_confirmed_total = (df_confirmed_total - df_confirmed_total.shift(1)).drop(df_confirmed_total.index[0])
        df_deaths_total = (df_deaths_total - df_deaths_total.shift(1)).drop(df_deaths_total.index[0])
        df_recovered_total = (df_recovered_total - df_recovered_total.shift(1)).drop(df_recovered_total.index[0])

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=df_confirmed_total.index, y=df_confirmed_total,
                            mode='lines+markers',
                            name='Confirmed',
                            line=dict(color='#3372FF', width=2),
                            fill='tozeroy',))
    fig.add_trace(go.Scatter(x=df_confirmed_total.index, y=df_recovered_total,
                            mode='lines+markers',
                            name='Recovered',
                            line=dict(color='#33FF51', width=2),
                            fill='tozeroy',))
    fig.add_trace(go.Scatter(x=df_confirmed_total.index, y=df_deaths_total,
                            mode='lines+markers',
                            name='Deaths',
                            line=dict(color='#FF3333', width=2),
                            fill='tozeroy',))

    fig.update_layout(
        hovermode='x',
        font=dict(
            family="Courier New, monospace",
            size=14,
            color=colors['figure_text'],
        ),
        legend=dict(
            x=0.02,
            y=1,
            traceorder="normal",
            font=dict(
                family="sans-serif",
                size=12,
                color=colors['figure_text']
            ),
            bgcolor=colors['background'],
            borderwidth=5
        ),
        paper_bgcolor=colors['background'],
        plot_bgcolor=colors['background'],
        margin=dict(l=0,
                    r=0,
                    t=0,
                    b=0
                    ),
        height=300,

    )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#3A3A3A')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#3A3A3A')

    fig.update_yaxes(zeroline=True, zerolinewidth=2, zerolinecolor='#3A3A3A')
    return fig




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
                             'textAlign': 'left',
                             'fontSize':'20px'
                         },
                         className='twelve columns'
                         ),
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
                html.P('New Cases: ' + f"{df_confirmed_total[7]:,d}",
                       style={
                    'textAlign': 'center',
                    'color': colors['confirmed_text'],
                    'backgroundColor': colors['background'],
                    'fontSize': 17,
                    'borderRadius': '10px',
                }
                ),
            ],
                style=divBorderStyle,
                className='three columns',
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
                html.P(f"{df_deaths_total[3]:,d}",
                       style={
                    'textAlign': 'center',
                    'color': colors['deaths_text'],
                    'fontSize': 30,
                    'backgroundColor': colors['background'],
                }
                ),
                 html.P('Mortality Rate: ' + str(round(df_deaths_total[3]/df_confirmed_total[1] * 100, 3)) + '%',
                       style={
                    'textAlign': 'center',
                    'color': colors['deaths_text'],
                    'backgroundColor': colors['background'],
                    'fontSize': 17,
                    'borderRadius': '10px',
                }
                ),
            ],
                style=divBorderStyle,
                className='three columns'),
             html.Div([
                html.H4(children='Active Cases: ',
                       style={
                           'textAlign': 'center',
                           'color': '#fb8dfc',
                           'backgroundColor': colors['background'],
                           'marginBottom':'0',
                       }
                       ),
                html.P(f"{df_active_total[4]:,d}",
                       style={
                    'textAlign': 'center',
                    'color': '#fb8dfc',
                    'fontSize': 30,
                    'backgroundColor': colors['background'],
                }
                ),
                 html.P('Growth Rate: ' + str(round(df_confirmed_total[7]/df_confirmed_total[1] * 100, 3)) + '%',
                       style={
                    'textAlign': 'center',
                    'color': '#fb8dfc',
                    'backgroundColor': colors['background'],
                    'fontSize': 17,
                    'borderRadius': '10px',
                }
                ),
            ],
                style=divBorderStyle,
                className='three columns'),
            html.Div([
                html.H4(children='Total Recovered: ',
                       style={
                           'textAlign': 'center',
                           'color': colors['recovered_text'],
                           'backgroundColor': colors['background'],
                           'marginBottom':'0',
                       }
                       ),
                html.P(f"{df_recovered_total[2]:,d}",
                       style={
                    'textAlign': 'center',
                    'color': colors['recovered_text'],
                    'backgroundColor': colors['background'],
                    'fontSize': 30,
                }
                ),
                 html.P('Recovery Rate: ' + str(round(df_recovered_total[2]/df_confirmed_total[1] * 100, 3)) + '%',
                       style={
                    'textAlign': 'center',
                    'color': colors['recovered_text'],
                    'backgroundColor': colors['background'],
                    'fontSize': 17,
                    'borderRadius': '10px',
                }
                ),
            ],
                style=divBorderStyle,
                className='three columns'),
        ], className='row'),
        html.Div([
            html.Div([

                html.P([html.Span('States with highest cases: ',
                                  ),
                        html.Br(),
                        ],
                       style={
                           'textAlign': 'center',
                           'color': 'rgb(200,200,200)',
                           'fontsize': 12,
                           'backgroundColor': '#18012e',
                           'borderRadius': '12px',
                           'fontSize': 17,
                       }
                       ),
                html.P(confirm_cases),
            ],
                className="three columns",
            ),

            html.Div([

                html.P([html.Span('States with highest mortality: ',
                                  ),
                        html.Br(),
                        ],
                       style={
                           'textAlign': 'center',
                           'color': 'rgb(200,200,200)',
                           'fontsize': 12,
                           'backgroundColor': '#18012e',
                           'borderRadius': '12px',
                           'fontSize': 17,
                       }
                       ),
                html.P(deaths_cases),
            ],
                className="three columns",
            ),
        ],),
        html.Div(
            [
                html.Div(
                    [
                        dt.DataTable(
                            data=map_data.to_dict('records'),
                            columns=[
                                {"name": i, "id": i, "deletable": False, "selectable": True} for i in ['State', 'Confirmed',
                                                                                                       'Deaths', 'Recovered']
                            ],
                            fixed_rows={'headers': True, 'data': 0},
                            style_header={
                                'backgroundColor': 'rgb(30, 30, 30)',
                                'fontWeight': 'bold'
                            },
                            style_cell={
                                'backgroundColor': 'rgb(100, 100, 100)',
                                'color': colors['text'],
                                'maxWidth': 0,
                                'fontSize':14,
                            },
                            style_table={
                                'maxHeight': '350px',
                                'overflowY': 'auto'
                            },
                            style_data={
                                'whiteSpace': 'normal',
                                'height': 'auto',

                            },
                            style_data_conditional=[
                                {
                                    'if': {'row_index': 'even'},
                                    'backgroundColor': 'rgb(60, 60, 60)',
                                },
                                {
                                    'if': {'column_id' : 'Confirmed'},
                                    'color':colors['confirmed_text'],
                                    'fontWeight': 'bold'
                                },
                                {
                                    'if': {'column_id' : 'Deaths'},
                                    'color':colors['deaths_text'],
                                    'fontWeight': 'bold'
                                },
                                {
                                    'if': {'column_id' : 'Recovered'},
                                    'color':colors['recovered_text'],
                                    'fontWeight': 'bold'
                                },
                                ],
                            style_cell_conditional=[
                                {'if': {'column_id': 'State'},
                                 'width': '26%'},
                                {'if': {'column_id': 'Confirmed'},
                                 'width': '16%'},
                                {'if': {'column_id': 'Deaths'},
                                 'width': '11%'},
                                {'if': {'column_id': 'Recovered'},
                                 'width': '16%'},
                            ],

                            editable=False,
                            filter_action="native",
                            sort_action="native",
                            sort_mode="single",
                            row_selectable="single",
                            row_deletable=False,
                            selected_columns=[],
                            selected_rows=[],
                            page_current=0,
                            page_size=1000,
                            id='datatable'
                        ),
                    ],
                    className="six columns"
                ),

            ], className="row",
        ),
        html.Div([
             html.Div([
                    html.Button(html.H6(children='For more news updates on Coronavirus',
                        id='news-button',
                        style={
                             'color': colors['text'],
                             'fontSize':'18px',
                             'lineHeight':'normal',
                             'textDecoration':'underline',
                         }
                         ),),

                ],className='twelve columns',),

                # Preload Modal windows and set "display": "none" to hide it first
                html.Div([  # modal div
                    html.Div([  # content div

                        dcc.Markdown('''
                           
                            Sources:
                            * World Health Organization (WHO): https://www.who.int/
                            * The Indian Express: https://indianexpress.com/article/india/coronavirus-india-live-news-updates-covid-19-tracker-total-corona-cases-in-india-covid-19-vaccine-update-6395797/
                            * The Economic Times: https://economictimes.indiatimes.com/news/coronavirus
                            * BNO News: https://bnonews.com/index.php/2020/02/the-latest-coronavirus-cases/
                            * NBC News: https://www.nbcnews.com/health/health-news/live-blog/2020-05-05-coronavirus-news-n1200041
                            * US CDC: https://www.cdc.gov/coronavirus/2019-ncov/index.html
                            * 1Point3Arces: https://coronavirus.1point3acres.com/en
                            * WorldoMeters: https://www.worldometers.info/coronavirus/
                            '''),
                        html.Hr(),
                        html.Button('Close', id='modal-close-button',
                        style={
                             'color': colors['text'],
                         },)
                    ],
                        style={
                            'fontSize': 10,
                            'lineHeight': 0.9,
                        },
                        className='modal-content',
                    ),
                ],
                    id='modal',
                    className='modal',
                    style={"display": "none"},
                ),
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


# hide/show modal
@app.callback(Output('modal', 'style'),
              [Input('news-button', 'n_clicks')])
def show_modal(n):
    if n > 0:
        return {"display": "block"}
    return {"display": "none"}

# Close modal by resetting info_button click to 0
@app.callback(Output('news-button', 'n_clicks'),
              [Input('modal-close-button', 'n_clicks')])
def close_modal(n):
    return 0


if __name__ == '__main__':
    app.run_server(debug=True)