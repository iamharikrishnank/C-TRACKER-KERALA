import dash

import dash_core_components as dcc
import dash_html_components as html
import plotly
import random
import plotly.graph_objs as go
import dash_table
import dash_html_components as html
import dash_core_components as dcc
import requests
import re
import folium
import pandas as pd
import os

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
wards=' '
wards=df.wards.tolist()
list=[]
list_popup=[]
case_url = 'https://keralastats.coronasafe.live/latest.json'
case_read = requests.get(case_url)
case_x = case_read.json()
df_case=pd.DataFrame(case_x['summary'])
df_case=df_case.transpose()
df_case['death']=df_case['confirmed']-df_case['active']-df_case['recovered']
df_case_today=pd.DataFrame(case_x['delta'])

df_case_today=df_case_today.transpose()
df_case_today['death']=df_case_today['confirmed']-df_case_today['active']-df_case_today['recovered']
active= str(df_case_today.active.sum())
recovered= str(df_case_today.recovered.sum())
confirmed= str(df_case_today.confirmed.sum())
death= str(df_case_today.death.sum())
if df_case_today.active.sum()>=0:
    active= '(' + '+' + active + ')'
else:
    active = str(0-df_case_today.active.sum())
    active = '(' + '-' + active + ')'
if df_case_today.recovered.sum()>=0:
    recovered= '('  + '+' + recovered + ')'
else:
    recovered = str(0-df_case_today.recovered.sum())
    recovered= '('  + '+' + recovered + ')'

if df_case_today.confirmed.sum()>=0:
    confirmed= '(' + '+' + confirmed + ')'
else:
    confirmed = str(0-df_case_today.confirmed.sum())
    confirmed= '(' + '+' + confirmed + ')'
if df_case_today.death.sum()>=0:
    death= '(' + '+' + death + ')'
else:
    death =  str(0-df_case_today.death.sum())
    death= '(' + '+' + death + ')'

data_case={'CONFIRMED': df_case.confirmed.sum(),'ACTIVE': df_case.active.sum(),'RECOVERED': df_case.recovered.sum(), 'DEATH': df_case.death.sum()}
data_case_today={'CONFIRMED': confirmed, 'ACTIVE': active,'RECOVERED': recovered,'DEATH': death}
data_case=pd.DataFrame(data_case,index=[0])
data_case_today=pd.DataFrame(data_case_today,index=[0])
def split_uppercase(value):
    return re.sub(r'([A-Z])', r' \1', value)
for i in range (0,len(df)):
    
    

    value = df.lsgd[i]
    jilla = df.district[i]
    wards = df.wards[i]
    
    sep = ' '
    
    res = re.sub(r"(\w)([A-Z])", r"\1 \2", value) + '  ' +jilla
    new_value=  res.split(sep, 1)[0] +  ','+jilla.split(sep, 1)[0]  + '   ' + 'wards:' + wards
    print(res)
    list.append(res)
    list_popup.append(new_value)
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

map_osm=folium.Map(location=[10.850516,76.271080], zoom_start=7.49, tiles='OpenStreetMap',max_bounds=True)
hotspot=folium.map.FeatureGroup()
state_boundaries = 'state.geojson'
folium.GeoJson(state_boundaries).add_to(map_osm)
district_geo='district.geojson'
folium.GeoJson(district_geo).add_to(map_osm)
for point in range(1,len(list_location)) :
      hotspot.add_child(
          folium.CircleMarker(
          list_location[point],radius =5,
          color = "Red", fill_color= "Red",
          
          popup=list_popup[point],
          )
      ) 
      map_osm.add_child(hotspot)

map_osm.save('map.html')
app = dash.Dash(__name__)
server = app.server
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}
app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='C-TRACKER KERALA DASH BOARD',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    html.Div(children='C-TRACKER KERALA: A web application  for tracking COVID-19 spread all over Kerala.', style={
        'textAlign': 'center',
        'color': colors['text']
    }),
        dash_table.DataTable(
    data=data_case.to_dict('records') + data_case_today.to_dict('records'),
    columns=[{'id': c, 'name': c} for c in data_case.columns],

    style_as_list_view=True,
    style_header={'backgroundColor': 'rgb(30, 30, 30)',
    		   'fontWeight': 'bold',
    		   'textAlign': 'center',
        	   'color': 'white',
    		   'font-family':'Times New Roman',
            	   'fontSize':28
            	   
    },
    
    style_cell={
        'backgroundColor': 'rgb(50, 50, 50)',
        'textAlign': 'center',
        'color': 'white',
        'fontWeight': 'bold',
        'font-family':'Times New Roman',
        'fontSize':28, 
        
    },
    ),
    
    html.H2(children='LATEST COVID-19 HOTSPOTS IN KERALA[UPDATED]', style={
        'textAlign': 'center',
        'color': colors['text']
    }),
    html.Iframe(id='map', srcDoc = open('map.html','r').read(), width='100%',height='600'),
    html.H2(children='COVID-19 POSITIVE CASES IN KERALA[UPDATED]', style={
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
    html.H2(children='COVID-19 DAILY TESTS  IN KERALA[UPDATED]', style={
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
    html.H2(children='COVID-19 DAILY POSITIVE CASES IN KERALA[UPDATED]', style={
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
