import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
from dash_table import DataTable
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import date
from datetime import datetime as dt
from Viz_scraping import run_scraping
import plotly.figure_factory as ff

df = pd.read_csv('df.csv')


def now():
    now = dt.now()
    str_now = (str(now.year) + '-' + str(now.month) + '-' + str(now.day))
    return str_now


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.css.append_css({"external_url": 'https://codepen.io/chriddyp/pen/bWLwgP.css'})
application = app.server
app.title = "Visualization Project"

app.layout = html.Div(children=[

    html.Div([

        html.Div([html.Br(), html.H1('Surveillance of air pollution in Denmark for the last 30 days',
                                     style={'margin-left': '30%', 'font-family': 'Helvetica'}), html.Br()]),
        # dropdown menu
        html.Div(children=[dcc.Dropdown(id='stationfilter',
                                        style={'height': '30px', 'width': '1500px', 'font-size': "95%",
                                               'font-family': 'Verdana'},
                                        options=[{'label': "All", 'value': "all"},
                                                 {'label': "Aarhus Botanisk Have", 'value': 'AARH6'},
                                                 {'label': "Aarhus Banegaardsgade", 'value': 'AARH3'},
                                                 {'label': "Aalborg Oesterbro", 'value': 'AALB5'},
                                                 {'label': "Aalborg Vesterbro", 'value': 'AALB4'},
                                                 {'label': "Ulfborg", 'value': 'ULGB'},
                                                 {'label': "Risoe", 'value': 'RISOE'},
                                                 {'label': "Foellesbjerg", 'value': 'FOEL'},
                                                 {'label': "Anholt", 'value': 'ANHO'},
                                                 {'label': "Odense Raadhus", 'value': 'ODEN2'},
                                                 {'label': "Odense, Groenlykkevej", 'value': 'ODEN6'},
                                                 {'label': "Jagtvej", 'value': 'JAGT1'},
                                                 {'label': "Hvidovre", 'value': 'HVID'},
                                                 {'label': "H. C. Andersens Boulevard", 'value': 'HCAB'},
                                                 {'label': "H. C. Oersted Instituttet", 'value': 'HCOE'}],
                                        multi=True,
                                        value='all')],
                 className='two columns'),
        html.Br(),
        html.Br(),

        # datepicker
        html.Div(children=[dcc.DatePickerRange(id='datepicker',
                                               style={'height': '30px', 'width': '330px', 'font-size': "85%",
                                                      'font-family': 'Verdana'},
                                               # clearable (boolean; default False): Whether or not the dropdown is "clearable",
                                               # that is, whether or not a small "x" appears on the right of the dropdown that
                                               # removes the selected value.
                                               clearable=True,
                                               # with_portal (boolean; default False): If True, calendar will open in
                                               # a screen overlay portal, not supported on vertical calendar
                                               with_portal=True,

                                               # DATE PICKING OPTIONS
                                               # minimum_nights (number; optional): Specifies a minimum number of nights that must be selected between the startDate and the endDate

                                               minimum_nights=0,
                                               # min_date_allowed (string; optional): Specifies the lowest selectable date for the component. Accepts datetime.datetime objects or strings in the format 'YYYY-MM-DD'
                                               min_date_allowed=df['date'][0],
                                               # max_date_allowed (string; optional): Specifies the highest selectable date for the component. Accepts datetime.datetime objects or strings in the format 'YYYY-MM-DD'
                                               max_date_allowed=now(),
                                               # start_date (string; optional): Specifies the starting date for the component. Accepts datetime.datetime objects or strings in the format 'YYYY-MM-DD'
                                               start_date=df['date'][0],
                                               # start_date_placeholder_text (string; optional): Text that will be displayed in the first input box of the date picker when no date is selected. Default value is 'Start Date'
                                               # start_date_placeholder_text='MMM Do, YY'
                                               # end_date (string; optional): Specifies the ending date for the component. Accepts datetime.datetime objects or strings in the format 'YYYY-MM-DD'
                                               end_date=now(),
                                               # end_date_placeholder_text (string; optional): Text that will be displayed in the second input box of the date picker when no date is selected. Default value is 'End Date'
                                               # end_date_placeholder_text='MMM Do, YY'

                                               # updatemode (a value equal to: 'singledate', 'bothdates'; default 'singledate'): Determines when the component should update its value.
                                               # If bothdates, then the DatePicker will only trigger its value when the user has finished picking both dates.
                                               # If singledate, then the DatePicker will update its value as one date is picked.
                                               # updatemode = 'bothdays',

                                               # display_format (string; optional): Specifies the format that the selected dates will be displayed valid formats are variations of "MM YY DD".
                                               # For example: "MM YY DD" renders as '05 10 97' for May 10th 1997 "MMMM, YY" renders as 'May, 1997' for May 10th 1997 "M, D, YYYY" renders as '07, 10, 1997'
                                               # for September 10th 1997 "MMMM" renders as 'May' for May 10 1997
                                               display_format='DD-MM-YYYY'

                                               )],
                 className='two columns'),

        html.Br(),
        html.Br(),
        html.Br(),

        # first column
        html.Div(children=[
            # first row
            html.Div(children=[
                html.Div([html.Br(), dcc.Graph(id='comparison_chart', style={'display': 'inline-block'}),
                          dcc.Checklist(id='pollutant_filter',
                                        style={'display': 'inline-block'},
                                        options=[
                                            {'label': 'NO2', 'value': 'NO2'},
                                            {'label': 'NOX', 'value': 'NOX'},
                                            {'label': 'CO', 'value': 'CO'},
                                            {'label': 'SO2', 'value': 'SO2'},
                                            {'label': 'O3', 'value': 'O3'},
                                            {'label': 'PM10 Teom', 'value': 'PM10 Teom'},
                                            {'label': 'PM2.5 Teom', 'value': 'PM2.5 Teom'},

                                        ],
                                        value=['NO2', 'NOX'], labelStyle={'display': 'inline-block'},
                                        className='eight columns'
                                        ),
                          # second row
                          html.Div(children=[html.Br(), dcc.Graph(id='piechart', style={'display': 'inline-block'})],
                                   className='twelve columns')],
                         className='three columns'),

                html.Div([html.Br(), dcc.Graph(id='barchart', style={'display': 'inline-block'}), html.Br(), html.Br(),
                          html.Br(), dcc.Graph(id='dist', style={'display': 'inline-block'})
                          ], className='three columns'),
                html.Div([html.Br(), dcc.Graph(id='map', style={'display': 'inline-block'})
                          ], className='six columns')],
                className='eleven columns')],
            className='eleven columns')

    ]),

    html.Div(children=[
        html.Div(children=[
            html.Div(children=[
                html.Br(), html.Br(), dcc.Graph(id='linegraph', style={'display': 'inline-block'}),
                html.Div(id='my_div', style={'margin-left': '7%'})],

                className='eight columns')],
            className='twelve columns')],
        className='twelve columns'),

    dcc.Interval(
        id='interval_component',
        interval=36000000,  # Every hour
        n_intervals=0,
    ),

])  # code above these brackets


############################ LAYOUT ################################################################
############################ LAYOUT ################################################################        
############################ LAYOUT ################################################################


@app.callback(Output('my_div', 'children'),
              [Input('interval_component', 'n_intervals')])
def live_update(n_intervals):
    now = dt.now()
    date_time = now.strftime("%d-%m-%Y %H:%M")
    return "Last update: {}".format(date_time)


############################ PIE CHART #############################################################

@app.callback(
    Output('piechart', 'figure'),
    [
        Input('stationfilter', 'value'),
        Input('datepicker', 'start_date'),
        Input('datepicker', 'end_date'),
        Input('interval_component', 'n_intervals')
    ])
def piechart(station, start_date, end_date, n_intervals):
    a = start_date.split('-')
    start = date(int(a[0]), int(a[1]), int(a[2]))
    b = end_date.split('-')
    end = date(int(b[0]), int(b[1]), int(b[2]))
    if type(station) == str:
        station = [station]
    if n_intervals == 0:
        df = pd.read_csv('df.csv')
    else:
        df = run_scraping(stations)
    df['date'] = pd.to_datetime(df['date'])
    df = df[df["location"].isin(station)]
    df = df[(df['date'] >= start)]
    df = df[(df['date'] <= end)]

    label = ["NOX", "NO2"]
    values = [df['NOX'].sum(), df['NO2'].sum()]

    pie = go.Figure(
        data=[
            go.Pie(
                labels=label,
                values=values,
                marker=dict(colors=['rgb(66,146,198)', 'rgb(102,194,164)']),
            )
        ]
    )

    pie.update_layout(title='Relationship of nitrogen oxide levels', width=410, height=410,
                      margin=dict(t=50, b=10, l=10, r=0)
                      )
    pie.update_layout(title_text='Relationship of nitrogen oxide levels', title_x=0.5, font_family="Helvetica",
                      title_font_color="rgb(82,82,82)",
                      font_size=13)

    return pie


############################  DISTRIBUTION PLOT ###################################################


@app.callback(
    Output('dist', 'figure'),
    [
        Input('stationfilter', 'value'),
        Input('datepicker', 'start_date'),
        Input('datepicker', 'end_date'),
        Input('interval_component', 'n_intervals')
    ])
def dist(station, start_date, end_date, n_intervals):
    a = start_date.split('-')
    start = date(int(a[0]), int(a[1]), int(a[2]))
    b = end_date.split('-')
    end = date(int(b[0]), int(b[1]), int(b[2]))
    if type(station) == str:
        station = [station]
    if n_intervals == 0:
        df = pd.read_csv('df.csv')
    else:
        df = run_scraping(stations)
    df['date'] = pd.to_datetime(df['date'])
    df = df[df["location"].isin(station)]
    df = df[(df['date'] >= start)]
    df = df[(df['date'] <= end)]

    x1 = df['NO2']
    x2 = df['NOX']

    hist_data = [x1, x2]
    group_labels = ['NO2', 'NOX']

    dist = ff.create_distplot(hist_data, group_labels, colors=['rgb(102,194,164)', 'rgb(66,146,198)'])

    dist.update_layout(title_text='Distribution of nitrogen oxide levels', template='none', height=410, width=430,
                       margin=dict(t=80, b=30, l=30, r=30), font_family="Helvetica", title_font_color="rgb(82,82,82)",
                       font_size=13)

    return dist


############################ BAR CHART ##############################################################

@app.callback(
    Output('barchart', 'figure'),
    [
        Input('stationfilter', 'value'),
        Input('datepicker', 'start_date'),
        Input('datepicker', 'end_date'),
        Input('interval_component', 'n_intervals')
    ])
def barchart(station, start_date, end_date, n_intervals):
    a = start_date.split('-')
    start = date(int(a[0]), int(a[1]), int(a[2]))
    b = end_date.split('-')
    end = date(int(b[0]), int(b[1]), int(b[2]))
    if type(station) == str:
        station = [station]
    if n_intervals == 0:
        df = pd.read_csv('df.csv')
    else:
        df = run_scraping(stations)
    df['date'] = pd.to_datetime(df['date'])
    df = df[df["location"].isin(station)]
    df = df[(df['date'] >= start)]
    df = df[(df['date'] <= end)]
    x = ['min NOX', 'Max NOX', 'min NO2', 'max NO2']
    y = [df['NOX'].min(), df['NOX'].max(), df['NO2'].min(), df['NO2'].max()]

    bar = go.Figure(
        data=[
            go.Bar(
                x=x,
                y=y,
                width=0.4,
                marker=dict(color=['rgb(66,146,198)', 'rgb(33,113,181)', 'rgb(102,194,164)', 'rgb(65,174,118)']),
            )
        ]
    )

    bar.update_layout(title='Minimum and maximum nitrogen oxide levels', yaxis_title='min/max in µg/m3', height=350,
                      width=400, template='none', margin=dict(t=30, b=30, l=30, r=30), font_family="Helvetica",
                      title_font_color="rgb(82,82,82)",
                      font_size=13)

    return bar


############################ LINE GRAPH #############################################################


@app.callback(
    Output('linegraph', 'figure'),
    [
        Input('stationfilter', 'value'),
        Input('datepicker', 'start_date'),
        Input('datepicker', 'end_date'),
        Input('interval_component', 'n_intervals')
    ])
def line2(station, start_date, end_date, n_intervals):
    start = np.datetime64(start_date)
    end = np.datetime64(end_date)
    if type(station) == str:
        station = [station]
    if n_intervals == 0:
        df = pd.read_csv('df.csv')
    else:
        df = run_scraping(stations)
    df['date'] = pd.to_datetime(df['date'])
    df = df[df["location"].isin(station)]
    df = df[(df['date'] >= start)]
    df = df[(df['date'] <= end)]
    df.index = df['Målt (starttid)']

    x = df["Målt (starttid)"].unique()
    if len(station) == 1:
        y1 = df["NOX"]
        y2 = df["NO2"]
    else:
        means_nox = pd.Series([0] * len(x), index=df['Målt (starttid)'].unique())
        means_no2 = pd.Series([0] * len(x), index=df['Målt (starttid)'].unique())
        for stat in station:
            adding_nox = pd.Series(df[df['location'] == stat]['NOX'],
                                   index=df[df['location'] == stat]['Målt (starttid)'])
            adding_no2 = pd.Series(df[df['location'] == stat]['NO2'],
                                   index=df[df['location'] == stat]['Målt (starttid)'])
            means_nox = means_nox.add(adding_nox, fill_value=0)
            means_no2 = means_no2.add(adding_no2, fill_value=0)
        y1 = means_nox.truediv(len(station))
        y2 = means_no2.truediv(len(station))

    limitvalues = {'Limit NOX': [30], 'Limit NO2': [200]}
    lim_no2 = limitvalues['Limit NO2'] * len(x)
    lim_nox = limitvalues['Limit NOX'] * len(x)

    line = go.Figure()

    colornox = [1 if v < 30 else -1
                for v in y1]
    colorscalenox = [[0, 'rgb(228,26,28)'], [1, 'rgb(4,90,141)']]

    # NOX
    line.add_trace(
        go.Scatter(
            x=x,
            y=y1,
            mode='lines+markers',
            name='NOX',
            marker={'color': colornox,
                    'colorscale': colorscalenox,
                    'size': 3},
            line=dict(color='rgb(4,90,141)'),
            connectgaps=False
        )
    )

    colorno2 = [1 if v < 200 else -1
                for v in y2]
    colorscaleno2 = [[0, 'rgb(228,26,28)'], [1, 'green']]

    # NO2
    line.add_trace(
        go.Scatter(
            x=x,
            y=y2,
            mode='lines+markers',
            name='NO2',
            marker={'color': colorno2,
                    'colorscale': colorscaleno2,
                    'size': 3},
            line=dict(color='rgb(102,194,164)'),
            connectgaps=False
        )
    )

    df['NOX_mean'] = df.groupby("time")["NOX"].transform('mean')
    y_nox_mean = df['NOX_mean'][:(len(x))]
    print(y_nox_mean)

    # NOX mean
    line.add_trace(
        go.Scatter(
            x=df['Målt (starttid)'],
            y=y_nox_mean,
            mode='lines',
            fill="tozeroy",
            name='NOX hourly mean',
            marker={'color': "rgb(66,146,198)", 'size': 0},
            line=dict(color="rgb(66,146,198)", width=0)
        )
    )

    df['NO2_mean'] = df.groupby("time")["NO2"].transform('mean')
    y_no2_mean = df['NO2_mean'][:(len(x))]
    print(y_no2_mean)

    # NO2 mean
    line.add_trace(
        go.Scatter(
            x=df['Målt (starttid)'],
            y=y_no2_mean,
            mode='lines',
            fill="tozeroy",
            name='NO2 hourly mean',
            marker={'color': "rgb(102,194,164)", 'size': 0},
            line=dict(color="rgb(102,194,164)", width=0)
        )
    )
    line.add_trace(
        go.Scatter(
            x=df['Målt (starttid)'],
            y=lim_nox,
            visible='legendonly',
            mode='lines',
            name='limit NOX',
            line=dict(color="rgb(227,74,51)", width=1, dash='dash')
        )
    )

    line.add_trace(
        go.Scatter(
            x=df['Målt (starttid)'],
            y=lim_no2,
            visible='legendonly',
            mode='lines',
            name='limit NO2',
            line=dict(color="rgb(179,0,0)", width=1, dash='dash')
        )
    )

    line.update_layout(title='Daily levels and daily mean levels of nitrogen oxide',
                       xaxis_title='Date and Time',
                       yaxis_title='NOX & NO2 in µg/m3', template='none', width=2050, height=450,
                       margin=dict(t=60, b=150, l=0, r=0), font_family="Helvetica")

    line.update_layout(
        font_family="Helvetica",
        title_font_family="Helvetica",
        title_font_color="rgb(82,82,82)",
        font_size=15
    )

    line.update_xaxes(tickangle=40, title_font={"size": 20}, title_standoff=40,
                      range=[df['date'].min(), df['date'].max()], constrain='domain')

    line.update_yaxes(title_standoff=40, scaleanchor="x", visible=False, scaleratio=1)

    return line


############################################### MAP ###########################################################
@app.callback(
    Output('map', 'figure'),
    [Input('interval_component', 'n_intervals')])
def map(n_intervals):
    if n_intervals == 0:
        df = pd.read_csv('df.csv')
    else:
        df = run_scraping(stations)
    df.fillna(0)
    df = df[df["type"] != 'all']
    # df = pd.to_datetime(df)
    positions = {'Arhus Botanisk Have': [56.159664, 10.193995, 'Bybaggrundsstation'],
                 'Aarhus Banegårdsgade': [56.150425, 10.200660, 'Gadestation'],
                 'Aalborg Østerbro': [57.046555, 9.933836, 'Bybaggrundsstation'],
                 'Aalborg Vesterbro': [57.050880, 9.916869, 'Gadestation'],
                 'Ulfborg': [56.290918, 8.431604, 'Landstation'],
                 'Risø': [55.694217, 12.088464, 'Landstation'],
                 'Føllesbjerg': [54.746643, 10.736298, 'Landstation'],
                 'Anholt': [56.716232, 11.516893, 'Landstation'],
                 'Odense Rådhus': [55.396160, 10.388922, 'Bybaggrundsstation'],
                 'Odense Grønløkkevej': [55.397451, 10.366918, 'Gadestation'],
                 'Kbh - Jagtvej': [55.698436, 12.553441, 'Gadestation'],
                 'Hvidovre': [55.632508, 12.462285, 'Bybaggrundsstation'],
                 'Kbh - H. C. Ørsted Instituttet': [55.700284, 12.560883, 'Bybaggrundsstation'],
                 'Kbh - H. C. Andersens Boulevard': [55.674673, 12.570635, 'Gadestation'],
                 }

    df_positions = pd.DataFrame.from_dict(positions, orient='index', columns=['lat', 'lon', 'type'])

    combined = df.drop_duplicates(subset=["location"], keep="first", inplace=False)
    sumNOX = df["NOX"].groupby(by=df['location']).sum()
    sumNO2 = df["NO2"].groupby(by=df['location']).sum()
    combined["location2"] = combined["location"]
    combined = combined.set_index("location2")
    combined["sumNO2"] = sumNO2
    combined["sumNOX"] = sumNOX

    print(combined)

    scattermap = px.scatter_mapbox(combined,
                                   lat="lat",
                                   lon="lon",
                                   zoom=6.1,
                                   width=800,
                                   height=700,
                                   size="sumNO2",
                                   size_max=45,
                                   title='Sum of nitrogen oxides',
                                   color="type",
                                   color_discrete_sequence=px.colors.qualitative.Prism,
                                   hover_name=df_positions.index,
                                   hover_data=["lat", "lon", "sumNO2", "type"])

    scattermap.update_layout(mapbox_style="carto-positron",
                             margin={"r": 0, "t": 0, "l": 0, "b": 0},
                             hoverlabel={'bgcolor': 'white', 'font_size': 16, 'font_family': 'Verdana'}
                             )

    # scattermap.update_layout(legend=dict(
    # orientation="h",
    # yanchor="bottom",
    # y=0,
    # xanchor="right",
    # x=0, ))

    return scattermap


############################################### BarChart2 ###########################################################


@app.callback(
    Output('comparison_chart', 'figure'),
    [Input('stationfilter', 'value'),
     Input('pollutant_filter', 'value'),
     Input('datepicker', 'start_date'),
     Input('datepicker', 'end_date'),
     Input('interval_component', 'n_intervals')
     ])
def barchart_2(value, pols, start_date, end_date, n_intervals):
    global colors
    a = start_date.split('-')
    start = date(int(a[0]), int(a[1]), int(a[2]))
    b = end_date.split('-')
    end = date(int(b[0]), int(b[1]), int(b[2]))
    if type(value) == str:
        value = [value]
    if n_intervals == 0:
        df = pd.read_csv('/Users/camilla/PycharmProjects/Viz/venv/df.csv')
    else:
        df = run_scraping(stations)

    df['date'] = pd.to_datetime(df['date'])
    pollutants = pols

    df = df[(df['date'] >= start)]
    df = df[(df['date'] <= end)]
    df = df[df['location'].isin(value)]

    list = []
    for i in pollutants:
        list.append(df.groupby(["location"], sort=False)[i].mean())

    color_discrete_map = {"HCAB": "rgb(191,211,230)",
                          "HCOE": "rgb(208, 217, 168)",
                          "HVID": "rgb(208, 229, 250)",
                          "JAGT1": "rgb(224, 254, 254)",
                          "ODEN6": "rgb(216, 246, 214)",
                          "ODEN2": "rgb(134, 174, 209)",
                          "ANHO": "rgb(127,205,187)",
                          "FOEL": "rgb(214, 247, 240)",
                          "RISOE": "rgb(183, 203, 192)",
                          "ULBG": "rgb(179, 238, 255)",
                          "AALB4": "rgb(210, 234, 203)",
                          "AALB5": "rgb(210, 216, 182)",
                          "AARH3": "rgb(218, 240, 238)",
                          "AARH6": "rgb(186, 226, 221)",
                          "all": "rgb(197, 193, 139)"}

    list_dataframe = pd.DataFrame(list)
    fig = px.bar(list_dataframe, x=pollutants,
                 y=value,
                 color_discrete_map=color_discrete_map,
                 title="Mean values of pollutant levels")

    fig.update_layout(title="Mean values of pollutant levels",
                      yaxis_title='mean in µg/m3',
                      barmode='group',
                      height=350,
                      width=450,
                      template='none',
                      margin=dict(t=30, b=30, l=30, r=30), font_family="Helvetica", title_font_color="rgb(82,82,82)",
                      font_size=13)

    return fig


if __name__ == '__main__':
    app.run_server(port=9004)

yanchor = "bottom",
y = 1.02,
xanchor = "right",
x = 1

labels = {
    'HCAB': "H. C. Andersens Boulevard",
    'HCOE': "H. C. Oersted Instituttet",
    'HVID': "Hvidovre",
    'JAGT1': "Jagtvej",
    'ODEN6': "Odense, Groenlykkevej",
    'ODEN2': "Odense Raadhus",
    'ANHO': "Anholt",
    'FOEL': "Foellesbjerg",
    'RISOE': "Risoe",
    'ULBG': "Ulfborg",
    'AALB4': "Aalborg Vesterbro",
    'AALB5': "Aalborg Oesterbro",
    'AARH3': "Aarhus Banegaardsgade",
    'AARH6': "Aarhus Botanisk Have",
    'all': 'All'
}

legend = dict(yanchor="top", y=0.88, xanchor="left", x=0.88)
