import dash
from dash.dependencies import Output, Event
import dash_core_components as dcc
import dash_html_components as html
import plotly
import random
import plotly.graph_objs as go
from collections import deque
import dash_html_components as html
import dash_core_components as dcc
import requests
import re
import folium
import pandas as pd
link = 'https://keralastats.coronasafe.live/testreports.json'
read = requests.get(link)
x1 = read.json()
df1=pd.DataFrame(x1['reports'])
date=df1['date']
testcase=df1['today']
postivecase=df1['positive']
today_positive=df1['today_positive']
url = 'https://keralastats.coronasafe.live/hotspots.json'
r = requests.get(url)
x = r.json()
df=pd.DataFrame(x['hotspots'])
data=df.lsgd

list=[]
def split_uppercase(value):
    return re.sub(r'([A-Z])', r' \1', value)
for i in range (0,len(df)):
    
    

    value = df.lsgd[i]
    jilla = df.district[i]
    
    sep = ' '
    
    res = re.sub(r"(\w)([A-Z])", r"\1 \2", value) + '  ' +jilla
    new_value=  res.split(sep, 1)[0] +jilla.split(sep, 1)[0] 
    print(res)
    list.append(res)
list_location=[]
URL = "https://geocode.search.hereapi.com/v1/geocode"

for a in list:
    print(a)
    location = a #taking user input
    api_key = 'MeIrhhrqJ0h9LaQ7euxAaRPCUokDr_7N0KUVYHd0O0M' # Acquire from developer.here.com
    PARAMS = {'apikey':api_key,'q':location} 

    # sending get request and saving the response as response object 
    r = requests.get(url = URL, params = PARAMS) 
    data = r.json()

    latitude = data['items'][0]['position']['lat']
    longitude = data['items'][0]['position']['lng']
    print(latitude,longitude)
    if (latitude==14.8856 and longitude==79.29639):
       

    	latitude = 11.87411
    	longitude = 75.37147
   
    list_location.append([latitude,longitude])

map_osm=folium.Map(location=[10.850516,76.271080], zoom_start=7.35, tiles='OpenStreetMap')
for point in range(1,len(list_location)) :
        
      folium.Marker(list_location[point], popup=list[point]).add_to(map_osm)



map_osm.save('map.html')
app = dash.Dash(__name__)
server = app.server
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}
app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='COVID-19 KERALA DASH BOARD',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    html.H2(children='LATEST HOTSPOTS IN KERALA[UPDATED]', style={
        'textAlign': 'center',
        'color': colors['text']
    }),
    html.Iframe(id='map', srcDoc = open('map.html','r').read(), width='100%',height='600'),
    html.H2(children='COVID 19 POSITIVE CASES IN KERALA[UPDATED]', style={
        'textAlign': 'center',
        'color': colors['text']
    }),
    dcc.Graph(
        id='Graph1',
        figure={
            'data': [
                {'x': date, 'y': postivecase, 'type': 'line', 'name': 'Postive Cases'},
                
              
                
            ],
            'layout': {
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                }
            }
        }
    ),
    html.H2(children='COVID 19 DAILY TESTS  IN KERALA[UPDATED]', style={
        'textAlign': 'center',
        'color': colors['text']
    }),
    dcc.Graph(
        id='Graph2',
        figure={
            'data': [
                {'x': date, 'y': testcase, 'type': 'line', 'name': 'Test Cases'},
                
              
                
            ],
            'layout': {
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                }
            }
        }
    ),
    html.H2(children='COVID 19 DAILY POSITIVE CASES IN KERALA[UPDATED]', style={
        'textAlign': 'center',
        'color': colors['text']
    }),
    dcc.Graph(
        id='Graph3',
        figure={
            'data': [
                {'x': date, 'y': today_positive, 'type': 'line', 'name': 'Daily Postive Cases'},
                
              
                
            ],
            'layout': {
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                }
            }
        }
    ),
])

if __name__ == '__main__':
    app.run_server(debug=True)
