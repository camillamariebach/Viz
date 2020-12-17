import pandas as pd
# pip install selenium
from selenium import webdriver


def get_table(urls):
    tables = []
    for key, value in urls.items():
        driver = webdriver.PhantomJS(executable_path="/Library/Frameworks/Python.framework/Versions/3.8/lib/phantomjs")
        driver.get(value[0])

        js = '''
        var done = arguments[0];
        console.log("testing1");
        var data = {};
        data.__RequestVerificationToken = $('#__AjaxAntiForgeryForm input[name=__RequestVerificationToken]').val();
        $.ajax({
            url: "%s",
            type: "POST",
            data: data,
            success: function (response) {
                done(response);
                return response;
            }
        });
        ''' % (value[1])
        # Return html table. Use e.g. the lxml library to parse the data.
        try:
            result = driver.execute_async_script(js)
            tables.append(result)
        except:
            continue
        driver.quit()
    return tables


def to_df(tables):
    df_tables = []
    for table in tables:
        x = pd.read_html(table, thousands='.', decimal=',')
        df_tables.append(x)
    return df_tables


def add_location(frame, dict_locations):
    row_names = dict_locations.keys()
    row_names_list = list(row_names)
    for i in range(len(frame)):
        loc = row_names_list[i]
        locations = [loc] * len(frame[i][0])
        frame[i][0].insert(loc=0, column='location', value=locations)
        lat = dict_locations[loc][2]
        lats = [lat] * len(frame[i][0])
        frame[i][0].insert(loc=0, column='lat', value=lats)
        lon = dict_locations[loc][3]
        lons = [lon] * len(frame[i][0])
        frame[i][0].insert(loc=0, column='lon', value=lons)
        stat = dict_locations[loc][4]
        stats = [stat] * len(frame[i][0])
        frame[i][0].insert(loc=0, column='type', value=stats)
    return frame


def con_data(d):
    li = []
    # FIXME: Noget med len(d)
    for i in range(len(d)):
        li.append(d[i][0])
    concat = pd.concat(li, sort=False)
    return concat


def split_date(dataframe):
    d = pd.to_datetime(dataframe['Målt (starttid)'], dayfirst=True)
    dataframe['date'] = d.dt.date
    dataframe['time'] = d.dt.time
    return dataframe


def add_all(f):
    df = f.drop(['type', 'lon', 'lat', 'location'], axis=1)
    df_mean = []
    for hour in df['Målt (starttid)'].unique():
        frame = df[df['Målt (starttid)'] == hour]
        mean = frame.mean().tolist()
        df_mean.append(mean)
    df_mean_df = pd.DataFrame(df_mean)
    df_mean_df.insert(loc=0, value=df['Målt (starttid)'].unique(), column='Målt (starttid)')
    df_mean_df.insert(loc=0, column='type', value=['all'] * len(df_mean_df))
    df_mean_df.insert(loc=0, column='lat', value=['NaN'] * len(df_mean_df))
    df_mean_df.insert(loc=0, column='lon', value=['NaN'] * len(df_mean_df))
    df_mean_df.insert(loc=0, column='location', value=['all'] * len(df_mean_df))
    return df_mean_df


def run_scraping(s):
    tables = get_table(s)
    d = to_df(tables)
    d = add_location(d, s)
    con = con_data(d)
    mean_data = add_all(con)
    mean_data_renamed = mean_data.rename(columns=dict(zip(mean_data.columns, con.columns)))
    t = con.append(mean_data_renamed)
    split = split_date(t)
    dataset = split.iloc[::-1]
    return dataset


"""
# TO BE SET INTO dcc.Interval
dcc.Interval(
    id='interval_component',
    interval=36000000,  # Every hour
    n_interval=0
)


# Some Div has to be the different graphs. We need to have multiple outputs
@app.callback(Output('some div', 'children'),
              [Input('interval_component', 'n_intervals')])
def update_some_div(n):
    return run_scraping(stations)


# Some Div has to be the different graphs. We need to have multiple outputs
@app.callback(Output('some div', 'children'),
              [Input('interval_component', 'n_intervals')])
def update_some_div(n):
    return run_scraping(stations)


# Some Div has to be the different graphs. We need to have multiple outputs
@app.callback(Output('some div', 'children'),
              [Input('interval_component', 'n_intervals')])
def update_some_div(n):
    return run_scraping(stations)
"""

if __name__ == "__main__":
    stations = {'HCAB': ["https://envs2.au.dk/Luftdata/Presentation/table/Copenhagen/HCAB",
                         "/Luftdata/Presentation/table/MainTable/Copenhagen/HCAB", 55.674673, 12.570635, 'Street Station'],
                'HCOE': ["https://envs2.au.dk/Luftdata/Presentation/table/Copenhagen/HC%C3%98",
                         "/Luftdata/Presentation/table/MainTable/Copenhagen/HC%C3%98", 55.700284, 12.560883,
                         'City Background Station'],
                'HVID': ["https://envs2.au.dk/Luftdata/Presentation/table/Copenhagen/HVID",
                         "/Luftdata/Presentation/table/MainTable/Copenhagen/HVID", 55.632508, 12.462285,
                         'City Background Station'],
                'JAGT1': ["https://envs2.au.dk/Luftdata/Presentation/table/Copenhagen/JAGT1",
                          "/Luftdata/Presentation/table/MainTable/Copenhagen/JAGT1", 55.698436, 12.553441,
                          'Street Station'],
                'ODEN6': ["https://envs2.au.dk/Luftdata/Presentation/table/Odense/ODEN6",
                          "/Luftdata/Presentation/table/MainTable/Odense/ODEN6", 55.397451, 10.366918, 'Street Station'],
                'ODEN2': ["https://envs2.au.dk/Luftdata/Presentation/table/Odense/ODEN2",
                          "/Luftdata/Presentation/table/MainTable/Odense/ODEN2", 55.396160, 10.388922,
                          'City Background Station'],
                'ANHO': ["https://envs2.au.dk/Luftdata/Presentation/table/Rural/ANHO",
                         "/Luftdata/Presentation/table/MainTable/Rural/ANHO", 56.716232, 11.516893, 'Rural Station'],
                'FOEL': ["https://envs2.au.dk/Luftdata/Presentation/table/Rural/FOEL",
                         "/Luftdata/Presentation/table/MainTable/Rural/FOEL", 54.746643, 10.736298, 'Rural Station'],
                'RISOE': ["https://envs2.au.dk/Luftdata/Presentation/table/Rural/RISOE",
                          "/Luftdata/Presentation/table/MainTable/Rural/RISOE", 55.694217, 12.088464, 'Rural Station'],
                'ULBG': ["https://envs2.au.dk/Luftdata/Presentation/table/Rural/ULBG",
                         "/Luftdata/Presentation/table/MainTable/Rural/ULBG", 56.290918, 8.431604, 'Rural Station'],
                'AALB4': ["https://envs2.au.dk/Luftdata/Presentation/table/Aalborg/AALB4",
                          "/Luftdata/Presentation/table/MainTable/Aalborg/AALB4", 57.050880, 9.916869, 'Street Station'],
                'AALB5': ["https://envs2.au.dk/Luftdata/Presentation/table/Aalborg/AALB5",
                          "/Luftdata/Presentation/table/MainTable/Aalborg/AALB5", 57.046555, 9.933836,
                          'City Background Station'],
                'AARH3': ["https://envs2.au.dk/Luftdata/Presentation/table/Aarhus/AARH3",
                          "/Luftdata/Presentation/table/MainTable/Aarhus/AARH3", 56.150425, 10.200660, 'Street Station'],
                'AARH6': ["https://envs2.au.dk/Luftdata/Presentation/table/Aarhus/AARH6",
                          "/Luftdata/Presentation/table/MainTable/Aarhus/AARH6", 56.159664, 10.193995,
                          'City Background Station']
                }
    # HCA Boulevard, HCØ inst, Hvidovre, Jagtvej, Grønlykkevej, Rådhus, Anholt, Føllesbjerg, Risø, Ulborg, Vesterbro,
    # Østerbro, Banegårdsgade, Botanisk Have
    df = run_scraping(stations)
    df.to_csv(r'df.csv')