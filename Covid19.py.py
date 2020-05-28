import pandas as pd
import numpy as np
import requests, json
import csv
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
import datetime
import dash_daq as daq

external_stylesheets = [dbc.themes.BOOTSTRAP, 'https://codepen.io/Ruheengl/pen/KKdLBOY.css',
                        'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Covid19 - India Dashboard Example'


colors = {
    'background': 'rgba(3,169,244,0.3)',
    'text': '#2d8af7',
    'figure_text': '#2d8af7',
    'confirmed_text': '#f09307',
    'deaths_text': '#f44336',
    'recovered_text': '#00a816',
    'highest_case_bg': 'rgba(3,169,244,0.3)',

}
# Creating custom style for local use
divBorderStyle = {
    'backgroundColor': 'rgba(3,169,244,0.3)',
    'borderRadius': '12px',
    'lineHeight': 0.9,
}

# Creating custom style for local use
boxBorderStyle = {
    'borderColor': 'rgba(3,169,244,0.3)',
    'borderStyle': 'solid',
    'borderRadius': '10px',
    'borderWidth': 2,
}

theme =  {
    'dark': True,
}

url_confirmed = 'https://api.covid19india.org/csv/latest/state_wise.csv'
# print(url_confirmed)

df_confirmed = pd.read_csv(url_confirmed)
df_deaths = pd.read_csv(url_confirmed)
df_recovered = pd.read_csv(url_confirmed)

# print(df_deaths)
# print(df_confirmed)
# print(type(df_confirmed))

# print(df_confirmed)
df_confirmed_total = df_confirmed.iloc[0]
# print(df_confirmed_total)
df_deaths_total = df_deaths.iloc[0]
# print(df_deaths_total)
df_recovered_total = df_recovered.iloc[0]

df_active_total = df_recovered.iloc[0]

total_time_wise = pd.read_csv("https://api.covid19india.org/csv/latest/case_time_series.csv")
# print(total_time_wise)

total_tested = pd.read_csv("https://api.covid19india.org/csv/latest/tested_numbers_icmr_data.csv")
# print(total_tested)

# for highest case
df_confirmed_sorted = df_confirmed.sort_values(by=df_confirmed.columns[1], ascending=False)[
    ['State', df_confirmed.columns[1]]]
df_recovered_sorted = df_recovered.sort_values(by=df_recovered.columns[2], ascending=False)[
    ['State', df_recovered.columns[2]]]
df_deaths_sorted = df_deaths.sort_values(by=df_deaths.columns[3], ascending=False)[['State', df_confirmed.columns[3]]]

# for past 24 hrs
df_confirmed_sorted_1 = df_confirmed.sort_values(by=df_confirmed.columns[7], ascending=False)[
    ['State', df_confirmed.columns[7]]]
df_recovered_sorted_1 = df_recovered.sort_values(by=df_recovered.columns[7], ascending=False)[
    ['State', df_recovered.columns[7]]]
df_deaths_sorted_1 = df_deaths.sort_values(by=df_deaths.columns[7], ascending=False)[['State', df_deaths.columns[7]]]

# for displaying highest count states
df_confirmed_sorted_1 = df_confirmed_sorted_1.iloc[1:, :]

# for daily datewise state data
state_daily_url = 'https://api.covid19india.org/csv/latest/state_wise_daily.csv'
df_state_daily = pd.read_csv(state_daily_url)
df_short = pd.read_csv('short_States.txt')

# df_state_confirmed = df_state_daily.iloc[0,2]
# df_state_confirmed.append(df_state_daily.iloc[3,2])
# print(df_state_confirmed)

gk = df_state_daily.groupby('Status')
df_daily_confirmed = gk.get_group('Confirmed')
df_daily_recovered = gk.get_group('Recovered')
df_daily_deceased = gk.get_group('Deceased')

date_list = df_daily_confirmed['Date']
# print(date_list)

df_daily_confirmed_total = df_daily_confirmed['TT']
df_daily_recovered_total = df_daily_recovered['TT']
df_daily_deceased_total = df_daily_deceased['TT']

df_daily_confirmed_mh = df_daily_confirmed['MH']
df_daily_recovered_mh = df_daily_recovered['MH']
df_daily_deceased_mh = df_daily_deceased['MH']


def high_cases(state, total):
    return html.P([html.Span(state + ' | ' + f"{int(total):,d}",
                             style={'backgroundColor': colors['highest_case_bg'], 'borderRadius': '6px',
                                    'color': colors['text'], }),

                   ]
                  )


noToDisplay = 8

confirm_cases = []
for i in range(noToDisplay):
    confirm_cases.append(high_cases(df_confirmed_sorted.iloc[i+1, 0], df_confirmed_sorted.iloc[i+1, 1]))

# confirm_cases_24hrs = []
# for i in range(noToDisplay):
#     confirm_cases_24hrs.append(high_cases(df_confirmed_sorted_1.iloc[i,0],df_confirmed_sorted_1.iloc[i,1]))

deaths_cases = []
for i in range(noToDisplay):
    deaths_cases.append(high_cases(df_deaths_sorted.iloc[i + 1, 0], df_deaths_sorted.iloc[i + 1, 1]))

# deaths_cases_24hrs = []
# for i in range(noToDisplay):
#     deaths_cases.append(high_cases(df_deaths_sorted_1.iloc[i,0],df_deaths_sorted_1.iloc[i,1]))

url_states = pd.read_csv('states.txt')
# print(url_states)

# Recreate required columns for map data
map_data = df_confirmed[["State"]]
map_data = map_data.iloc[1:]

map_data = map_data.drop([10])


Latitude = url_states['Latitude'].tolist()
Longitude = url_states['Longitude'].tolist()
map_data['Latitude'] = Latitude
map_data['Longitude'] = Longitude

#print(map_data)


map_data['Confirmed'] = df_confirmed.loc[1:, df_confirmed.columns[1]]
map_data['Deaths'] = df_deaths.loc[:, df_deaths.columns[3]]
map_data['Recovered'] = df_recovered.loc[:, df_recovered.columns[2]]

# last 24 hours increase
map_data['Deaths_24hr'] = df_deaths_sorted_1.iloc[1:, 1]
map_data['Recovered_24hr'] = df_recovered_sorted_1.iloc[1:, 1]
map_data['Confirmed_24hr'] = df_confirmed_sorted_1.iloc[1:, 1]
map_data.sort_values(by='Confirmed', ascending=False, inplace=True)

# Variable For first graph
state_wise_daily = pd.read_csv("https://api.covid19india.org/csv/latest/state_wise_daily.csv")

state_wise_daily_confirmed = state_wise_daily[state_wise_daily.index % 3 == 0]
state_wise_daily_confirmed = state_wise_daily_confirmed.iloc[:, :3]
cols = state_wise_daily_confirmed.columns.tolist()
cols = cols[:-2] + cols[-1:]
state_wise_daily_confirmed = state_wise_daily_confirmed[cols]
list_of_dates = state_wise_daily_confirmed['Date'].to_list()
state_wise_daily_confirmed.columns = [''] * len(state_wise_daily_confirmed.columns)
state_wise_daily_confirmed = state_wise_daily_confirmed.iloc[:, 1]

state_wise_daily_recovered = state_wise_daily[state_wise_daily.index % 3 == 1]
state_wise_daily_recovered = state_wise_daily_recovered.iloc[:, :3]
cols = state_wise_daily_recovered.columns.tolist()
cols = cols[:-2] + cols[-1:]
state_wise_daily_recovered = state_wise_daily_recovered[cols]
state_wise_daily_recovered.columns = [''] * len(state_wise_daily_recovered.columns)
state_wise_daily_recovered = state_wise_daily_recovered.iloc[:, 1]

state_wise_daily_deaths = state_wise_daily[state_wise_daily.index % 3 == 2]
state_wise_daily_deaths = state_wise_daily_deaths.iloc[:, :3]
cols = state_wise_daily_deaths.columns.tolist()
cols = cols[:-2] + cols[-1:]
state_wise_daily_deaths = state_wise_daily_deaths[cols]
state_wise_daily_deaths.columns = [''] * len(state_wise_daily_deaths.columns)
state_wise_daily_deaths = state_wise_daily_deaths.iloc[:, 1]

# Data preprocessing for graph for top 10 highest confirmed and deceased cases in states

state_wise_daily_highest = pd.read_csv("https://api.covid19india.org/csv/latest/state_wise_daily.csv")
state_wise_daily_confirmed_10 = state_wise_daily_highest[state_wise_daily_highest.index % 3 == 0]

state_wise_daily_confirmed_10.drop(['Status', 'TT'], axis=1, inplace=True)
state_wise_daily_confirmed_10.set_index("Date", inplace=True)
state_wise_daily_confirmed10 = state_wise_daily_confirmed_10.sort_values(by=state_wise_daily_confirmed_10.index[-3],
                                                                         axis=1, ascending=False).iloc[:, :10]

state_wise_confirmed_stack = state_wise_daily_confirmed10.stack()
state_wise_confirmed_stack = state_wise_confirmed_stack.reset_index(level=[0, 1])
state_wise_confirmed_stack.rename(columns={'level_1': 'States', 0: "Confirmed"}, inplace=True)
# print(state_wise_confirmed_stack)

state_wise_daily_deaths_10 = state_wise_daily_highest[state_wise_daily_highest.index % 3 == 2]
state_wise_daily_deaths_10.drop(['Status', 'TT'], axis=1, inplace=True)
state_wise_daily_deaths_10.set_index("Date", inplace=True)
state_wise_daily_deaths10 = state_wise_daily_deaths_10.sort_values(by=state_wise_daily_deaths_10.index[-3], axis=1,
                                                                   ascending=False).iloc[:, :10]
state_wise_deaths_stack = state_wise_daily_deaths10.stack()
state_wise_deaths_stack = state_wise_deaths_stack.reset_index(level=[0, 1])
state_wise_deaths_stack.rename(columns={'level_1': 'States', 0: "Deceased"}, inplace=True)
# print(state_wise_deaths_stack)


total_tested = pd.read_csv("https://api.covid19india.org/csv/latest/tested_numbers_icmr_data.csv")
# print(total_tested)

#############################################################################
# mapbox_access_token keys, not all mapbox function require token to function.
#############################################################################
mapbox_access_token = 'pk.eyJ1IjoiMTExODAzMTU3IiwiYSI6ImNrOWliY3kzZDAwM2wzbHBqOHhqbnBwcHcifQ.hCWC05VqD38sJxDYlHGR8Q'

##################################################
# Variables for Zone
##################################################
content = requests.get("https://api.covid19india.org/zones.json")
json = json.loads(content.content)

zones = json['zones']
# print(zones)
# print(json)

f = open("test.csv", "w")

csv_writer = csv.writer(f)

count = 0

for zone in zones:

    if count == 0:
        header = zone.keys()
        csv_writer.writerow(header)
        count += 1

    csv_writer.writerow(zone.values())

f.close()

district_zone = pd.read_csv("test.csv")

district_zone = district_zone.drop(["source"], axis=1)

dist_col = district_zone['district'].to_list()


####################################################
# Prepare plotly figure to attached to dcc component
# Global outbreak Plot
####################################################
# Change date index to datetimeindex and share x-axis with all the plot
def draw_global_graph(state_wise_daily_confirmed, state_wise_daily_deaths, state_wise_daily_recovered,
                      graph_type='Total Cases'):
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=list_of_dates, y=state_wise_daily_confirmed,
                             mode='lines+markers',
                             name='Confirmed',
                             line=dict(color='#3372FF', width=2),
                             fill='tozeroy', ))
    fig.add_trace(go.Scatter(x=list_of_dates, y=state_wise_daily_recovered,
                             mode='lines+markers',
                             name='Recovered',
                             line=dict(color='#32a856', width=2),
                             fill='tozeroy', ))
    fig.add_trace(go.Scatter(x=list_of_dates, y=state_wise_daily_deaths,
                             mode='lines+markers',
                             name='Deaths',
                             line=dict(color='#FF3333', width=2),
                             fill='tozeroy', ))

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
        paper_bgcolor='rgba(0,188,212,0.1)',
        plot_bgcolor='rgba(0,188,212,0.1)',
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


####################################################
# Function to plot Highest 10 countries cases
####################################################
def draw_highest_10(state_wise_confirmed_stack, state_wise_deaths_stack, graphHigh10_type='Confirmed Cases'):
    if graphHigh10_type == 'Confirmed Cases':
        fig = px.line(state_wise_confirmed_stack, x="Date", y="Confirmed", color='States',
                      color_discrete_sequence=px.colors.qualitative.Light24)
    else:
        fig = px.line(state_wise_deaths_stack, x="Date", y="Deceased", color='States',
                      title='Deceased cases', color_discrete_sequence=px.colors.qualitative.Light24)

    fig.update_layout(
        xaxis_title=None,
        yaxis_title=None,
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
                size=9,
                color=colors['figure_text']
            ),
        ),
        paper_bgcolor='rgba(0,188,212,0.1)',
        plot_bgcolor='rgba(0,188,212,0.1)',
        margin=dict(l=0,
                    r=0,
                    t=0,
                    b=0
                    ),
        height=300,

    )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#3A3A3A')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#3A3A3A')

    # fig.update_xaxes(zeroline=True, zerolinewidth=2, zerolinecolor='#3A3A3A')
    fig.update_yaxes(zeroline=True, zerolinewidth=2, zerolinecolor='#3A3A3A')
    return fig


####################################################
# Function to plot Single Country Scatter Plot
####################################################

def draw_singleState_Scatter(df_daily_confirmed, df_daily_deceased, df_daily_recovered, state, selected_row=0):
    df_state = df_short.loc[df_short['Full'].isin(state)]

    dfl = df_state['Short'].values.tolist()
    state_index = dfl[0]

    df_confirmed_t = df_daily_confirmed[state_index]
    df_recovered_t = df_daily_recovered[state_index]
    df_deaths_t = df_daily_deceased[state_index]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=date_list, y=df_confirmed_t,
                             mode='lines+markers',
                             name='Confirmed',
                             line=dict(color='#3372FF', width=2),
                             fill='tozeroy', ))
    fig.add_trace(go.Scatter(x=date_list, y=df_recovered_t,
                             mode='lines+markers',
                             name='Recovered',
                             line=dict(color='#32a856', width=2),
                             fill='tozeroy', ))
    fig.add_trace(go.Scatter(x=date_list, y=df_deaths_t,
                             mode='lines+markers',
                             name='Deceased',
                             line=dict(color='#FF3333', width=2),
                             fill='tozeroy', ))

    dfl2 = df_state['Full'].values.tolist()
    title = dfl2[0]
    # new = df_recovered_t.columns[selected_row].split("|", 1)
    # if new[0] == 'nann':
    #     title = new[1]
    # else:
    #     title = new[1] + " - " + new[0]

    fig.update_layout(
        title=title + ' (Daily Cases)',
        hovermode='x',
        font=dict(
            family="Courier New, monospace",
            size=14,
            color=colors['figure_text'],
        ),
        legend=dict(
            # x=0.02,
            # y=1,
            traceorder="normal",
            font=dict(
                family="sans-serif",
                size=12,
                color=colors['figure_text']
            ),
            #bgcolor=colors['background'],
            borderwidth=5
        ),
        paper_bgcolor='rgba(0,188,212,0.1)',
        plot_bgcolor='rgba(0,188,212,0.1)',
        margin=dict(l=0,
                    r=0,
                    t=65,
                    b=0
                    ),
        height=350,

    )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#3A3A3A')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#3A3A3A')

    fig.update_yaxes(zeroline=True, zerolinewidth=2, zerolinecolor='#3A3A3A')
    return fig


###########################
# functions to create map
###########################
def gen_map(map_data, zoom, lat, lon):
    return {
        "data": [{
            "type": "scattermapbox",  # specify the type of data to generate, in this case, scatter map box is used
            "lat": list(map_data['Latitude']),  # for markers location
            "lon": list(map_data['Longitude']),
            # "hoverinfo": "text",
            "hovertext": [["State: {} <br>Confirmed: {} <br>Deaths: {} <br>Recovered: {} ".format(j, k, l, m, )]
                          for j, k, l, m in zip(map_data['State'],
                                                map_data['Confirmed'], map_data['Deaths'], map_data['Recovered'])],

            "mode": "markers",
            "name": list(map_data['State']),
            "marker": {
                "opacity": 0.7,
                "size": np.log(map_data['Confirmed']) * 4,
            }
        },

        ],
        "layout": dict(
            autosize=True,
            height=350,
            font=dict(color=colors['figure_text']),
            titlefont=dict(color=colors['text'], size='14'),
            margin=dict(
                l=0,
                r=0,
                b=0,
                t=0
            ),
            hovermode="closest",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            legend=dict(font=dict(size=10), orientation='h'),
            mapbox=dict(
                accesstoken=mapbox_access_token,
                style='mapbox://styles/mapbox/dark-v10',
                center=dict(
                    lon=lon,
                    lat=lat,

                ),
                zoom=zoom,
            )
        ),
    }


####################################################
# Function to plot Single Country Bar with scatter Plot
####################################################

def draw_singleState_Bar(df_daily_confirmed, df_daily_deceased, df_daily_recovered, state, selected_row=0,
                         graph_line='Line Chart'):
    df_state = df_short.loc[df_short['Full'].isin(state)]

    dfl = df_state['Short'].values.tolist()
    state_index = dfl[0]

    df_confirmed_t = df_daily_confirmed[state_index]
    df_recovered_t = df_daily_recovered[state_index]
    df_deaths_t = df_daily_deceased[state_index]

    fig = go.Figure()

    fig.add_trace(go.Bar(x=date_list, y=df_confirmed_t,
                         name='Confirmed',
                         marker_color='#3372FF'
                         ))
    fig.add_trace(go.Bar(x=date_list, y=df_recovered_t,
                         name='Recovered',
                         marker_color='#32a856'
                         ))
    fig.add_trace(go.Bar(x=date_list, y=df_deaths_t,
                         name='Deceased',
                         marker_color='#FF3333'
                         ))

    dfl2 = df_state['Full'].values.tolist()
    title = dfl2[0]

    fig.update_layout(
        title=title + ' (Bar Graph) ',
        barmode='stack',
        hovermode='x',
        font=dict(
            family="Courier New, monospace",
            size=14,
            color=colors['figure_text'],
        ),
        legend=dict(
            traceorder="normal",
            font=dict(
                family="sans-serif",
                size=12,
                color=colors['figure_text']
            ),
            #bgcolor=colors['background'],
            borderwidth=5
        ),
        paper_bgcolor='rgba(0,188,212,0.1)',
        plot_bgcolor='rgba(0,188,212,0.1)',
        margin=dict(l=0, r=0, t=65, b=0),
        height=350,
    )

    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#3A3A3A')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#3A3A3A')

    fig.update_yaxes(zeroline=True, zerolinewidth=2, zerolinecolor='#3A3A3A')

    return fig

rootLayout = html.Div([

        # Header display
        html.Div(
            [
                html.H1(children='Public Health Monitoring and Surviellance System ',
                        style={
                            'textAlign': 'center',
                            'color': colors['text'],
                            'backgroundColor': colors['background'],
                            'fontFamily': 'Archia',
                            'fontSize': '50px',
                        },
                        className='twelve columns',
                        ),
                html.H1(children='Covid-19 (Coronavirus) Interactive Outbreak Tracker',
                        style={
                            'textAlign': 'center',
                            'color': colors['text'],
                            'backgroundColor': colors['background'],
                            'fontFamily': 'Archia',
                            'fontSize': '30px',
                        },
                        className='ten columns',
                        ),
                html.Div(children='Best viewed on Desktop. Refresh browser for latest update.',
                         style={
                             'textAlign': 'left',
                             'color': colors['text'],
                             'textAlign': 'left',
                             'fontSize': '20px'
                         },
                         className='twelve columns'
                         ),
                html.Div([html.Span('Last Updated: ',
                             style={'color': colors['text'],
                                    'fontSize':'17px',
                             }),
                        html.Span( state_wise_daily.iloc[-1]['Date'] + '  00:01 (UTC).',
                             style={'color': '#ebe705',
                             'fontWeight': 'bold',

                             }),

                         ],className='twelve columns'
                ),

                html.Div([html.Span('Total Samples tested till date: ',
                                    style={'color': colors['text'],
                                           'fontSize': '17px',
                                           }),
                          html.Span(total_tested.iloc[-1]['Total Samples Tested'],
                                    style={'color': '#ebe705',
                                           'fontWeight': 'bold',

                                           }),
                          html.Hr(),

                          ], className='twelve columns'
                         ),
            ], className="row"
        ),
        # First row display of total cases in India
        html.Div([
            html.Div(
                [
                    html.H4(children='Total Cases: ',
                            style={
                                'textAlign': 'center',
                                'color': colors['confirmed_text'],
                                #'backgroundColor': colors['background'],
                                'marginBottom': '0',

                            }
                            ),
                    html.P(f"{df_confirmed_total[1]:,d}",
                           style={
                               'textAlign': 'center',
                               'color': colors['confirmed_text'],
                               #'backgroundColor': colors['background'],
                               'fontSize': 30,
                           }
                           ),
                    html.P('New Cases: ' + f"{df_confirmed_total[7]:,d}",
                           style={
                               'textAlign': 'center',
                               'color': colors['confirmed_text'],
                               #'backgroundColor': colors['background'],
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
                            #'backgroundColor': colors['background'],
                            'marginBottom': '0',
                        }
                        ),
                html.P(f"{df_deaths_total[3]:,d}",
                       style={
                           'textAlign': 'center',
                           'color': colors['deaths_text'],
                           'fontSize': 30,
                           #'backgroundColor': colors['background'],
                       }
                       ),
                html.P('Mortality Rate: ' + str(round(df_deaths_total[3] / df_confirmed_total[1] * 100, 3)) + '%',
                       style={
                           'textAlign': 'center',
                           'color': colors['deaths_text'],
                           #'backgroundColor': colors['background'],
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
                            'color': '#7f02c2',
                            #'backgroundColor': colors['background'],
                            'marginBottom': '0',
                        }
                        ),
                html.P(f"{df_active_total[4]:,d}",
                       style={
                           'textAlign': 'center',
                           'color': '#7f02c2',
                           'fontSize': 30,
                           #'backgroundColor': colors['background'],
                       }
                       ),
                html.P('Growth Rate: ' + str(
                    round(total_time_wise.iloc[-1]['Daily Confirmed'] / df_confirmed_total[1] * 100, 3)) + '%',
                       style={
                           'textAlign': 'center',
                           'color': '#7f02c2',
                           #'backgroundColor': colors['background'],
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
                            #'backgroundColor': colors['background'],
                            'marginBottom': '0',
                        }
                        ),
                html.P(f"{df_recovered_total[2]:,d}",
                       style={
                           'textAlign': 'center',
                           'color': colors['recovered_text'],
                           #'backgroundColor': colors['background'],
                           'fontSize': 30,
                       }
                       ),
                html.P('Recovery Rate: ' + str(round(df_recovered_total[2] / df_confirmed_total[1] * 100, 3)) + '%',
                       style={
                           'textAlign': 'center',
                           'color': colors['recovered_text'],
                           #'backgroundColor': colors['background'],
                           'fontSize': 17,
                           'borderRadius': '10px',
                       }
                       ),
            ],
                style=divBorderStyle,
                className='three columns'),
        ], className='row'),

        html.Br(),
        # State cases and mortality rate
        html.Div([
            html.Div([

                html.P([html.Span('States with highest cases: ',
                                  ),
                        html.Br(),
                        ],
                       style={
                           'textAlign': 'centre',
                           'color': colors['text'],
                           'fontsize': 12,
                           'backgroundColor': colors['background'],
                           'borderRadius': '12px',
                           'fontSize': 17,
                       }
                       ),
                html.P(confirm_cases),
            ],
                className="six columns",
            ),
            html.Div([

                html.P([html.Span('States with highest mortality: ',
                                  ),
                        html.Br(),
                        ],
                       style={
                           'textAlign': 'centre',
                           'color': colors['text'],
                           'fontsize': 12,
                           'backgroundColor': colors['background'],
                           'borderRadius': '12px',
                           'fontSize': 17,
                       }
                       ),
                html.P(deaths_cases),
            ],
                className="six columns",
            ),
        ], ),
        # Graph of total confirmed, recovered and deaths
        html.Div(
            [
                html.H4(children='Covid-19 cases',
                        style={
                            'textAlign': 'center',
                            'color': colors['text'],
                            'backgroundColor': colors['background'],

                        },
                        className='twelve columns'
                        ),
                html.Div([
                    dcc.RadioItems(
                        id='graph-type',
                        options=[{'label': 'Total Cases', 'value': 'Total Cases'}],
                        value='Total Cases',
                        labelStyle={'display': 'inline-block'},
                        style={
                            'fontSize': 20,
                        },

                    )
                ], className='six columns'
                ),
                html.Div([
                    dcc.RadioItems(
                        id='graph-high10-type',
                        options=[{'label': i, 'value': i}
                                 for i in ['Confirmed Cases', 'Deceased Cases']],
                        value='Confirmed Cases',
                        labelStyle={'display': 'inline-block'},
                        style={
                            'fontSize': 20,
                        },

                    )
                ], className='five columns'
                ),

                html.Div([
                    dcc.Graph(
                        id='global-graph',

                    )
                ], className='six columns'
                ),
                html.Div([
                    dcc.Graph(
                        id='high10-graph',

                    )
                ], className='five columns'
                ),

            ], className="row",
            style={
                'textAlign': 'left',
                'color': colors['text'],
                #'backgroundColor': colors['background'],
            },
        ),

        html.Div([
            html.Div(children='India Outbreak Map - Select row from table to locate in map',
                     style={
                         'textAlign': 'center',
                         'color': colors['text'],
                         'backgroundColor': colors['background'],
                     },
                     className='six columns'
                     ),
        ], className='row'
        ),

        # scroll table and map graph
        html.Div(
            [

                html.Div(
                    [
                        dcc.Graph(id='map-graph',
                                  )
                    ], className="six columns"
                ),

                html.Div(
                    [
                        dt.DataTable(
                            data=map_data.to_dict('records'),
                            columns=[
                                {"name": i, "id": i, "deletable": False, "selectable": True} for i in
                                ['State', 'Confirmed',
                                 'Deaths', 'Recovered']
                            ],
                            fixed_rows={'headers': True, 'data': 0},
                            style_header={
                                'backgroundColor': '#0f011c',
                                'fontWeight': 'bold'
                            },
                            style_cell={
                                'backgroundColor': '#360166',
                                'color': colors['text'],
                                'maxWidth': 0,
                                'fontSize': 14,
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
                                    'backgroundColor': '#6402bd',
                                },
                                {
                                    'if': {'column_id': 'Confirmed'},
                                    'color': colors['confirmed_text'],
                                    'fontWeight': 'bold'
                                },
                                {
                                    'if': {'column_id': 'Deaths'},
                                    'color': colors['deaths_text'],
                                    'fontWeight': 'bold'
                                },
                                {
                                    'if': {'column_id': 'Recovered'},
                                    'color': colors['recovered_text'],
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
                            selected_rows=[0],
                            page_current=0,
                            page_size=1000,
                            id='datatable'
                        ),
                    ],
                    className="six columns"
                ),

            ], className="row",
        ),

        # Single state line graph, single state bar graph
        html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(id='line-graph',
                                  )
                    ], className="six columns"
                ),
                html.Div(
                    [
                        dcc.Graph(id='bar-graph',
                                  )
                    ], className="six columns"
                ),

            ], className="row",
            style={
                'textAlign': 'left',
                'color': colors['text'],
                #'backgroundColor': colors['background'],
            },
        ),
        html.Div([
            html.Div([html.P()], className='six columns'),  # leave a gap of 6 columns
            html.Div([
                dcc.RadioItems(
                    id='graph-line',

                )
            ], className="six columns"),

        ], className="row"
        ),


        html.Div([
            html.H4(children='Bar Chart Race',
                        style={
                            'textAlign': 'center',
                            'color': colors['text'],
                            'backgroundColor': colors['background'],

                        },
                        className='twelve columns'
                        ),
            html.Script(src='https://public.flourish.studio/resources/embed.js'),
            html.Iframe(src='https://flo.uri.sh/visualisation/2487975/embed', width='1240', height='400'),

        ], className="flourish-embed flourish-bar-chart-race",
        ),

        html.Br(),
        #adding zone map
        html.Div(children='For zone wise information: ',
             style={
                 'textAlign': 'center',
                 'color': '#f7f37e',
                 'fontSize': '20px',
                 'backgroundColor': '#000000',

             },
             className='twelve columns'
        ),

        # check the zone of your district
        html.Div([
            html.Div([
                html.Label('Enter the district name:'),
                dcc.Input(
                    id='District',
                    placeholder='Enter here',
                    type='text',
                    value='',
                    style={
                        'color': colors['text'],
                        'fontSize': '18px',
                        'lineHeight': 'normal',
                        'textDecoration': 'underline',
                    }
                ),
            ]),
            html.Br(),
            html.Div([
                html.Div(id='zone')
            ]),

         ]),
        #iframe for zone map
        html.Div([
            html.Script(src='https://public.flourish.studio/resources/embed.js'),
            html.Iframe(src='https://flo.uri.sh/visualisation/2197081/embed', width='1000', height='800'),

        ], className="flourish-embed flourish-map",
        ),

        #faq chatbot
        html.Div([
            html.Br(),
            html.A("Frequently Asked Questions", target="_blank",
                   style={
                       'color': colors['text'],
                       'fontSize': '24px',
                       'lineHeight': 'normal',
                   }),
            html.Br(),
        ]),
        html.Div([
            html.Iframe(src='https://node-red-drboh.eu-gb.mybluemix.net/ui/', width='1240', height='600'),

        ], className="twelve columns",
        ),

        html.Br(),
        # adding more related links
        html.Div([
            html.Div([
                html.Br(),
                html.Button(html.H6(children='For more news updates on Coronavirus',
                                    id='news-button',
                                    style={
                                        'color': colors['text'],
                                        'fontSize': '18px',
                                        'lineHeight': 'normal',
                                        'textDecoration': 'underline',
                                    }
                                    ), ),

            ], className='twelve columns', ),

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
                                }, )
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


    ]
)

app.layout = html.Div(
    html.Div(id='dark-theme-container', children=[

    html.Div(id='dark-theme-components', children=[
        daq.DarkThemeProvider(theme=theme, children=rootLayout)
    ], style={'border': 'solid 1px #A2B1C6', 'border-radius': '5px', 'padding': '20px', 'margin-top': '5px'}),

     html.Br(),

    daq.ToggleSwitch(
        id='toggle-theme',
        label=['Light', 'Dark'],
        value=True,
        style={'width' : '250px', 'margin' : 'auto'}
    ),

], style={'padding': '50px'})

)


#For first graph
@app.callback(
    Output('global-graph', 'figure'),
    [Input('graph-type', 'value')])
def update_graph(graph_type):
    fig_global = draw_global_graph(state_wise_daily_confirmed,state_wise_daily_deaths,state_wise_daily_recovered,graph_type)
    return fig_global

#Highest 10 states graph
@app.callback(
    Output('high10-graph', 'figure'),
    [Input('graph-high10-type', 'value')])
def update_graph_high10(graph_high10_type):
    fig_high10 = draw_highest_10(state_wise_confirmed_stack, state_wise_deaths_stack, graph_high10_type)
    return fig_high10

#Map and single state graph
@app.callback(
    [Output('map-graph', 'figure'),
    Output('line-graph', 'figure'),
    Output('bar-graph', 'figure')],
    [Input('datatable', 'data'),
     Input('datatable', 'selected_rows'),
     Input('graph-line','value')])
def map_selection(data,selected_rows,graph_line):
    aux = pd.DataFrame(data)
    aux.Latitude = url_states.loc[:, url_states.columns[1]]
    aux.Longitude = url_states.loc[:, url_states.columns[2]]
    temp_df = aux.iloc[selected_rows, :]
    zoom = 3

    zoom = 4
    string = temp_df['State'].iloc[0]
    dfb = next(iter(url_states[url_states['Place'] == string].index), 'no match')
    latitude = url_states.at[dfb, 'Latitude']
    longitude = url_states.at[dfb, 'Longitude']
    fig1 = draw_singleState_Scatter(df_daily_confirmed, df_daily_deceased, df_daily_recovered, temp_df['State'],
                                    selected_rows[0])
    fig2 = draw_singleState_Bar(df_daily_confirmed, df_daily_deceased, df_daily_recovered, temp_df['State'],
                                selected_rows[0], graph_line)
    return gen_map(aux, zoom, latitude, longitude), fig1, fig2

#for zone
@app.callback(
    Output('zone', 'children'),
    [Input('District', 'value')]
)
def find_zone(District):
    for d in dist_col:
        if District == d:
            index = dist_col.index(d)
            return "The zone is : ",district_zone.iloc[index][5]



# hide/show modal
@app.callback(Output('modal', 'style'),
              [Input('news-button', 'n_clicks')])
def show_modal(n):
    
    if (n > 0):
        return {"display": "block"}
    else:
        return {"display": "none"}

      
# Close modal by resetting info_button click to 0
@app.callback(Output('news-button', 'n_clicks'),
              [Input('modal-close-button', 'n_clicks')])
def close_modal(n):
    return 0

#For theme changing
@app.callback(
    dash.dependencies.Output('dark-theme-components', 'children'),
    [dash.dependencies.Input('toggle-theme', 'value')]
)
def edit_theme(dark):

    if(dark):
        theme.update(
            dark=True
        )
    else:
        theme.update(
            dark=False
        )
    return daq.DarkThemeProvider(theme=theme, children=rootLayout)

@app.callback(
    dash.dependencies.Output('dark-theme-components', 'style'),
    [dash.dependencies.Input('toggle-theme', 'value')],
    state=[dash.dependencies.State('dark-theme-components', 'style')]
)
def switch_bg(dark, currentStyle):
    if(dark):
        currentStyle.update(
            backgroundColor='black'
        )
    else:
        currentStyle.update(
            backgroundColor='white'
        )
    return currentStyle




if __name__ == '__main__':
    app.run_server(debug=True)
