import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import plotly.figure_factory as ff
from dash.dependencies import Input, Output, State
import json
import pandas as pd
import plotly_express as px
from datetime import datetime as dt
import dill
import requests

external_stylesheets = ['https://codepen.io/plotly/pen/EQZeaW.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv('dash_clean.csv')

df['fire_count'] = 1
df['county_fips'] = df['county_fips'].astype(str).apply(lambda x: '0'+x if len(x) == 4 else x)
data_total = df.groupby(['county_fips']).sum().reset_index()[['fire_size','fire_count', 'county_fips']]
econ_impact = pd.read_csv('economic_impact.csv')

fire_size = [ 30, 60, 120, 250, 550, 1500]
fire_count = [ 10, 50, 100, 200, 300, 400]

colorscale = ["#f7fbff", "#ebf3fb", "#deebf7", "#d2e3f3", "#c6dbef", "#b3d2e9", "#9ecae1",
    "#85bcdb", "#6baed6", "#57a0ce", "#4292c6", "#3082be", "#2171b5", "#1361a9",
    "#08519c", "#0b4083", "#08306b"
]

reds = ['#d1aad2','#d189c2','#dc62ad','#e23990','#d61c6c','#b70b50','#b20a4d']
blues = ["#f7fbff", "#d2e3f3", "#b3d2e9", "#9ecae1", "#3082be", "#2171b5",  "#08306b"]
teals = ['#9cd1d2','#80c3c2','#66b3b2','#4da5a4','#349695','#258586','#157576']
tealblues = ['#9dd3d1','#81c3cb','#65b3c2','#45a2b9','#368fae','#347da0','#306a93']
G10 = px.colors.qualitative.G10


YEARS = [1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, \
		2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016]

BINS = ['0-2', '2.1-4', '4.1-6', '6.1-8', '8.1-10', '10.1-12', '12.1-14', \
		'14.1-16', '16.1-18', '18.1-20', '20.1-22', '22.1-24',  '24.1-26', \
		'26.1-28', '28.1-30', '>30']

DEFAULT_COLORSCALE = ["#2a4858", "#265465", "#1e6172", "#106e7c", "#007b84", \
	"#00898a", "#00968e", "#19a390", "#31b08f", "#4abd8c", "#64c988", \
	"#80d482", "#9cdf7c", "#bae976", "#d9f271", "#fafa6e"]
DEFAULT_OPACITY = 0.8

results = ['Burning Scale','Potential Cause','Economic Damage']

with open('rfmodel_smote.dill', 'rb') as in_strm:
    rf_smote = dill.load(in_strm)

with open('gbrt_smote.dill', 'rb') as in_strm:
    gbrt_smote = dill.load(in_strm)

with open('rfmodel_smote_cause_v2.dill', 'rb') as in_strm:
    rf_cause = dill.load(in_strm)


styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

app.layout = html.Div(children=[
    html.Div([
        html.H1(
            children='Wildfire Risk and Information System',
            style={
                'textAlign': 'center',
                'color': '#306a93'
            }
        ),
        html.Div([
            html.Div([
                html.P('Drag the slider to change the year:'),
            ]),

            html.Div([
                dcc.Slider(
                    id='years-slider',
                    min=min(YEARS),
                    max=max(YEARS),
                    value=2016,
                    marks={str(year): str(year) for year in YEARS}
                        ),
                    ], style={'width':800, 'margin':20, 'color': '#306a93'}),
                ], style={'width':'five columns'}),

        html.Br(),

        dcc.Dropdown(
            options=[{'label': 'Acres Burned(single year)', 'value': 'fire_size'},
                     {'label': 'Wildfire Count (single year)', 'value': 'fire_count'}
                     ],
            value='fire_size',
            id='value-selected',
            style={'width': '50%','margin': 30}
        ),
        html.Div([
            html.Div([
                dcc.Graph(
                    id='state'
                )
            ], className = 'six columns'),
            html.Div([

                dcc.Graph(
                    id='county_choropleth'
                )
            ], className = "six columns")
        ], className = "row"),

        html.Div([
            html.Div([
                dcc.Dropdown(
                    options=[{'label': 'Arson', 'value': 'Arson'},
                             {'label': 'Campfire', 'value': 'Campfire'},
                             {'label': 'Children', 'value': 'Children'},
                             {'label': 'Debris Burning', 'value': 'Debris Burning'},
                             {'label': 'Equipment Use', 'value': 'Equipment Use'},
                             {'label': 'Fireworks', 'value': 'Fireworks'},
                             {'label': 'Lightning', 'value': 'Lightning'},
                             {'label': 'Powerline', 'value': 'Powerline'},
                             {'label': 'Railroad', 'value': 'Railroad'},
                             {'label': 'Smoking', 'value': 'Smoking'},
                             {'label': 'Structure', 'value': 'Structure'},
                             {'label': 'Miscellaneous', 'value': 'Miscellaneous'},
                             {'label': 'Missing/Undefined', 'value': 'Missing/Undefined'}
                             ],
                    value='Lightning',
                    id='reason-selected',
                    style={'width': '80%', 'margin': 30}
                )
            ], className = 'six columns'),

            html.Div([
                dcc.Dropdown(
                    options=[{'label': 'Acres Burned(single year)', 'value': 'fire_size'},
                             {'label': 'Wildfire Count (single year)', 'value': 'fire_count'}
                             ],
                    value='fire_size',
                    id='metric-selected',
                    style={'width': '80%', 'margin': 30}
                )
            ], className = "six columns")
        ], className = "row"),

        html.Div([
            html.Div([
                dcc.Graph(
                    id='state_reason'
                )
            ], className = 'six columns'),
            html.Div([
                dcc.Graph(
                    id='cause_breakdown'
                )
            ], className = "six columns")
        ], className = "row"),

        html.Div([
            html.Div([
                html.Div([
                    dcc.Input(
                        id ='lat',
                        placeholder='Enter Latitude...',
                        type='number',
                        value=''
                    ),
                    dcc.Input(
                        id = 'lon',
                        placeholder='Enter Longitude...',
                        type='number',
                        value=''
                    )
                ], style={'margin': 30}),

                html.Div([
                    html.P('Drag the slider to select drought level (5 is the most severe):'),
                        ], style={'margin': 30}),

                html.Div([
                    dcc.Slider(
                        id='drought-slider',
                        min=0,
                        max=5,
                        value=0,
                        marks={i: '{}'.format(i) for i in range(6)}
                    ),
                ], style={'width': 600, 'margin': 30, 'color': '#306a93'}),

                dcc.Dropdown(
                    options=[
                             {'label': 'Random Forest', 'value': 'RF'},
                             {'label': 'Gradient Boosting Regression Trees', 'value': 'GBRT'}

                             ],
                    value='RF',
                    id='model-selected',
                    style={'width': '60%', 'margin': 30}
                ),

                dcc.DatePickerSingle(
                    id='date-picker-single',
                    date=dt(1997, 5, 10),
                    style={'margin': 30}
                ),

                html.Button('Submit', id='button')
            ], className='six columns'),

            html.Div([
                dcc.Graph(
                    id = 'result_chart',
                            className='six columns')
            ], className='row')

        ])

])
], style={'backgroundColor':'white'})

@app.callback(Output("state", "figure"),
                [Input("value-selected", "value"),
                 Input("years-slider", "value")])

def update_figure(selected, year):
    def title(text):
        if text == "fire_size":
            return "Wildfire "+"Acres Burned"+" by States"
        elif text == "fire_count":
            return "Wildfire Count "+"by States"
        else:
            return "FIRE"
    if year == 2016:
        state_df = df.groupby(['state']).sum().reset_index()
    else:
        df_f = df[df['fire_year'] == year]
        state_df = df_f.groupby(['state','fire_year']).sum().reset_index()
    trace = go.Choropleth(locations=state_df['state'],
                          locationmode='USA-states',
                          z=state_df[selected],
                          text=state_df['state'],
                          autocolorscale=False,
                          colorscale="Blues",
                          reversescale=False,
                          marker={'line': {'color': 'rgb(180,180,180)','width': 0.5}},
                          colorbar={"thickness": 10,"len": 0.4,"x": -0.1,"y":0.7, "xanchor":'left'
                                    }) #'title': {"text": title(selected), "side":"top"}
    return {"data": [trace],
            "layout": go.Layout(title={'text': title(selected),'yanchor': 'top', 'x': 0.5, 'y':0.9},
                                clickmode='event+select',
                                paper_bgcolor='white',
                                plot_bgcolor='white',
                                height=600, width=800,
                                geo={'scope':'usa','bgcolor':'rgba(0,0,0,0)'},
                                margin=dict(
                                    l=0,
                                    r=0,
                                    b=0,
                                    t=0,
                                    pad=0
                                            )
                                )
            }

@app.callback(
    Output("county_choropleth", "figure"),
    [Input("value-selected", "value"),
     Input("years-slider", "value"),
     Input('state', 'clickData')])
def update_county(selected, year, clickData):
    def title(text):
        if text == "fire_size":
            return "Wildfire "+"Acres Burned at "+ state_selected
        elif text == "fire_count":
            return "Wildfire Count at "+ state_selected
        else:
            return "FIRE"

    county_df = df[df['state'] == 'CA']
    state_selected = 'CA'
    if clickData:
        state_selected = clickData['points'][0]['text']
        county_df = df[df['state'] == state_selected]

    if year == 2016:
        county = county_df.groupby(['county_fips']).sum().reset_index()[['fire_size','fire_count', 'county_fips']]
        county_fips = county['county_fips'].to_list()
        value = county[selected].to_list()
    else:
        county_year = county_df[county_df['fire_year'] == year]
        county = county_year.groupby(['county_fips','fire_year']).sum().reset_index()
        county_fips = county['county_fips'].to_list()
        value = county[selected].to_list()

    if selected == 'fire_size':
        endpts = fire_size
    else:
        endpts = fire_count

    figure = ff.create_choropleth(fips=county_fips,
                                  values=value,
                                  scope=[state_selected],
                                  binning_endpoints=endpts, colorscale=blues,
                                  show_state_data=True,
                                  show_hover=True,
                                  asp=2,
                                  paper_bgcolor='white',
                                  plot_bgcolor='white',
                                  round_legend_values=True,
                                  title_text=title(selected),
                                  title={'yanchor': 'top', 'x': 0.5, 'y': 0.9},
                                  county_outline={'color': 'rgb(255,255,255)', 'width': 0.1},
                                  legend={'x': 0, 'y': 0.9},
                                  exponent_format=True,
                                  margin=dict(
                                              l=50,
                                              r=0,
                                              b=0,
                                              t=100,
                                              pad=0
                                            )
                                 )
    return (figure)

@app.callback(
    dash.dependencies.Output("state_reason", "figure"),
    [Input("metric-selected", "value"),
     Input("reason-selected", "value"),
     Input("years-slider", "value")])

def update_figure(selected, cause, year):
    def title(text):
        if text == "fire_size":
            return "Acres Burned"
        elif text == "fire_count":
            return "Wildfire Count"
        else:
            return "FIRE"
    if year == 2016:
        state_df = df.groupby(['state','stat_cause_descr']).sum().reset_index()
    else:
        df_f = df[df['fire_year'] == year]
        state_df = df_f.groupby(['state','fire_year','stat_cause_descr']).sum().reset_index()

    trace = go.Choropleth(locations=state_df[state_df['stat_cause_descr'] == cause]['state'],
                          locationmode='USA-states',
                          z=state_df[state_df['stat_cause_descr'] == cause][selected],
                          text=state_df[state_df['stat_cause_descr'] == cause]['state'],
                          autocolorscale=False,
                          colorscale="Reds",
                          reversescale=False,
                          marker={'line': {'color': 'rgb(180,180,180)','width': 0.5}},
                          colorbar={"thickness": 10,
                                    "len": 0.4,"x": -0.1,"y":0.7,
                                    "xanchor":'left',
                                    'title': {"text": title(selected), "side":"top"}
                                    })
    return {"data": [trace],
            "layout": go.Layout(title={'text': 'Wildfire Caused By '+cause, 'yanchor': 'top', 'x': 0.5, 'y': 0.9},
                                clickmode='event+select',
                                paper_bgcolor='white',
                                plot_bgcolor='white',
                                height=600, width=800,
                                geo={'scope': 'usa', 'bgcolor': 'rgba(0,0,0,0)'},
                                margin=dict(
                                            l=0,
                                            r=0,
                                            b=0,
                                            t=0,
                                            pad=0
                                            )
                                )
            }

@app.callback(
    dash.dependencies.Output("cause_breakdown", "figure"),
    [Input("metric-selected", "value"),
     Input('state_reason', 'clickData')
     ])

def update_figure(selected, clickData):
    def size(text):
        if text == "fire_size":
            return 60
        elif text == "fire_count":
            return 20
        else:
            return 20

    def chart_title(text):
        if text == "fire_size":
            return "Acres Burned"
        elif text == "fire_count":
            return "Wildfire Count"
        else:
            return "FIRE"
    def title(text):
        if text == "fire_size" and clickData:
            return 'Wildfire Acres Burned at ' + state_selected
        elif text == "fire_count" and clickData:
            return 'Wildfire Count at ' + state_selected
        else:
            return 'Wildfire ' + chart_title(selected)

    state_df = df.groupby(['state','stat_cause_descr','fire_year']).sum().reset_index()
    # state_selected = 'CA'
    if clickData:
        state_selected = clickData['points'][0]['text']
        cause_data = state_df[state_df['state'] == state_selected]
    else:
        cause_data = df.groupby(['stat_cause_descr', 'fire_year']).sum().reset_index()[['fire_size', 'fire_year', 'stat_cause_descr', 'fire_count']]

    if selected is None:
        selected = 'fire_size'


    fig = px.scatter(cause_data, x="fire_year", y="stat_cause_descr", color="stat_cause_descr",
                             size=selected, size_max=size(selected),
                             labels=dict(stat_cause_descr='', fire_year=''),
                             range_x=[1991, 2018],
                             title={'text': title(selected), 'yanchor': 'top', 'x': 0.5, 'y': 0.9},
                             template='plotly_white',
                             color_discrete_sequence=G10).for_each_trace(lambda t: t.update(name=''))

    return (fig)

@app.callback(Output("result_chart", "figure"),
              [Input('button', 'n_clicks')],
              [State("lat", "value"),
               State("lon", "value"),
               State("drought-slider", "value"),
               State("model-selected", "value"),
               State("date-picker-single", "date")])

def update_figure(n_clicks, lat, lon, drought, model, date):

    year = int(date.split(' ')[0][:4])
    month = int(date.split(' ')[0][5:7])
    drought_input = float(drought * 20)
    lat = 40.967200
    lon = -117.784200

    y_test = [[lat, lon, month, year, drought_input]]

    if model == 'RF':
        y_pred = rf_smote.predict(y_test)
    elif model == 'GBRT':
        y_pred = gbrt_smote.predict(y_test)

    cause_test = [[lat, lon, month, year, drought_input, y_pred[0]]]
    cause_pred = rf_cause.predict(cause_test)

    params = {'lat': lat,
              'lon': lon}
    response_area = requests.get('https://geo.fcc.gov/api/census/area', params=params)
    county_fips = response_area.json()['results'][0]['county_fips']

    econ_dmg = int(econ_impact[econ_impact['fips'] == int(county_fips)]['economic_damage'])

    trace = go.Bar(x=results, y=[y_pred[0], cause_pred[0], econ_dmg])
    return {"data": [trace],
            "layout": go.Layout(title={'text': 'Prediction', 'yanchor': 'top', 'x': 0.5, 'y': 1},
                                paper_bgcolor='white',
                                plot_bgcolor='white',
                                yaxis={'tickvals': [1, 2, 3]}
                                )
            }

if __name__ == '__main__':
    app.run_server(debug=True)

