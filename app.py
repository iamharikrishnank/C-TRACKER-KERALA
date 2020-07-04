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
df_case['death']=df_case['deceased']
sorted_df_case=df_case.sort_values(by=['total_obs'], ascending=False)
sorted_active_case=df_case.sort_values(by=['active'], ascending=False)
df_case_today=pd.DataFrame(case_x['delta'])

df_case_today=df_case_today.transpose()
df_case_today['death']=df_case_today['deceased']
active= str(df_case_today.active.sum())
recovered= str(df_case_today.recovered.sum())
confirmed= str(df_case_today.confirmed.sum())
death= str(df_case_today.death.sum())
total= str(df_case_today.total_obs.sum())
hospital= str(df_case_today.hospital_obs.sum())
home= str(df_case_today.home_obs.sum())
recover= str(df_case_today.hospital_today.sum())
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
if df_case_today.total_obs.sum()>=0:
    total= '(' + '+' + total + ')'
else:

    total = '('  + total + ')'
if df_case_today.home_obs.sum() >= 0:
    home = '(' + '+' + home + ')'
else:

    home = '(' + home + ')'

if df_case_today.hospital_obs.sum() >= 0:
    hospital = '(' + '+' + hospital + ')'
else:

    hospital = '(' + hospital + ')'
if df_case_today.hospital_today.sum() >= 0:
    recover = '(' + '+' + recover + ')'
else:

    recover = '(' + recover + ')'

data_case={'ACTIVE': df_case.active.sum(),'RECOVERED': df_case.recovered.sum(),'CONFIRMED': df_case.confirmed.sum(), 'DEATH': df_case.death.sum()}
data_case_today={'ACTIVE': active,'RECOVERED': recovered,'CONFIRMED': confirmed, 'DEATH': death}
test_case={'TOTAL': df_case.total_obs.sum(),'HOSPITAL': df_case.hospital_obs.sum(),'HOME': df_case.home_obs.sum(), 'HOSPITALISED':df_case.hospital_today.sum()
}
test_case_today={'TOTAL': total,'HOSPITAL': hospital,'HOME': home, 'HOSPITALISED': recover}
test_report={'TOTAL': df1.total.iloc[-1],'TODAY': df1.today.iloc[-1],'POSITIVE': df1.positive.iloc[-1], 'POSTIVE TODAY': df1.today_positive.iloc[-1]
}
data_case=pd.DataFrame(data_case,index=[0])
data_case_today=pd.DataFrame(data_case_today,index=[0])
test_case=pd.DataFrame(test_case,index=[0])
test_case_today=pd.DataFrame(test_case_today,index=[0])
test_report=pd.DataFrame(test_report,index=[0])

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
    if (latitude>14.8856 and longitude>79.29639):
       location=re.sub(r"(\w)([A-Z])", r"\1 \2", value) + '  ' +'Kerala'

    	latitude = data['items'][0]['position']['lat']
    	longitude = data['items'][0]['position']['lng']
   
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
history_url = 'https://keralastats.coronasafe.live/histories.json'
history_read = requests.get(history_url)
history_x = history_read.json()
histories=history_x['histories']
date_history=pd.DataFrame(histories)
df_date=pd.DataFrame(date_history.date)
df_daily=pd.DataFrame(date_history.date)
list_active=[]
list_confirmed=[]
list_recovered=[]
list_death=[]
for i in date_history.index:
    df_history=pd.DataFrame.from_dict(date_history.summary.iloc[i])
    df_history=df_history.transpose()
    active=df_history.active.sum()
    confirmed=df_history.confirmed.sum()
    recovered=df_history.recovered.sum()
    death=df_history.deceased.sum()
    list_active.append(active)
    list_confirmed.append(confirmed)
    list_recovered.append(recovered)
    list_death.append(death)
df_date['active']=pd.DataFrame(list_active)
df_date['recovered']=pd.DataFrame(list_recovered)
df_date['confirmed']=pd.DataFrame(list_confirmed)
df_date['death']=pd.DataFrame(list_death)
list_active_daily=[]
list_confirmed_daily=[]
list_recovered_daily=[]
list_death_daily=[]
for i in date_history.index:
    df_history_daily=pd.DataFrame.from_dict(date_history.delta.iloc[i])
    df_history_daily=df_history_daily.transpose()
    active=df_history_daily.active.sum()
    confirmed=df_history_daily.confirmed.sum()
    recovered=df_history_daily.recovered.sum()
    death=df_history_daily.deceased.sum()
    list_active_daily.append(active)
    list_confirmed_daily.append(confirmed)
    list_recovered_daily.append(recovered)
    list_death_daily.append(death)
df_daily['active']=pd.DataFrame(list_active_daily)
df_daily['recovered']=pd.DataFrame(list_recovered_daily)
df_daily['confirmed']=pd.DataFrame(list_confirmed_daily)
df_daily['death']=pd.DataFrame(list_death_daily)
app = dash.Dash(__name__)
server = app.server
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}
fig = go.Figure(data=[go.Bar(
    x=sorted_df_case.index,
    y=sorted_df_case.total_obs,
    marker=dict(
        color=sorted_df_case.total_obs,

        showscale=True,


    ),



    width=[.70,.65,.60,.55,.50,.45,.40,.35,.30,.25,.20,.15,.10,.05],




)])
fig.update_layout(
    
    height=600,
    title="Quarantine Summary",
    xaxis_title="Districts",
    yaxis_title="Number of Cases",
    plot_bgcolor= colors['background'],
    paper_bgcolor= colors['background'],
    font=dict(
        family="Courier New, monospace",
        size=18,
        color=colors['text']
    ),
    yaxis_showgrid=False,
)
fig_stack = go.Figure(data=[
    go.Bar(name='Active', x=sorted_active_case.index, y=sorted_active_case.active),
    go.Bar(name='Death', x=sorted_active_case.index, y=sorted_active_case.death)
])
# Change the bar mode
fig_stack.update_layout(barmode='stack',
        
        height=600,
        title="Districtwise Active-Death Summary",
        xaxis_title="Districts",
        yaxis_title="Number of Cases",
        plot_bgcolor = colors['background'],
        paper_bgcolor = colors['background'],
        font=dict(
        family="Courier New, monospace",
        size=18,
        color=colors['text']
        ),
        yaxis_showgrid=False,


)
    
app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='C-TRACKER KERALA DASH BOARD',
        style={
            'textAlign': 'center',
            'color': colors['text'],
            
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
    dcc.Graph(
        id='covid history',
        figure={
            'data': [
                {'x': df_date.date, 'y': df_date.active, 'type': 'line', 'name': 'Active'},
                {'x': df_date.date, 'y': df_date.confirmed, 'type': 'line', 'name': 'Confirmed'},
                {'x': df_date.date, 'y': df_date.recovered, 'type': 'line', 'name': 'Recovered'},
                {'x': df_date.date, 'y': df_date.death, 'type': 'line', 'name': 'Death'},

            ],
            'layout': {
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'title':"Cumulative Summary of Kerala",
                'font': {
                    'color': colors['text'],
                    'family':"Courier New, monospace",
                    'size':18
                }
            }
        }
    ),
    dcc.Graph(
        id='covid daily',
        figure={
            'data': [
                
                {'x': df_daily.date, 'y': df_daily.confirmed, 'type': 'scatter', 'name': 'Confirmed','mode':'lines+markers',},
                {'x': df_daily.date, 'y': df_daily.recovered, 'type': 'scatter', 'name': 'Recovered','mode':'lines+markers',},
                {'x': df_daily.date, 'y': df_daily.death, 'type': 'scatter', 'name': 'Death','mode':'lines+markers'},

            ],
            'layout': {
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'title':"Datewise Reporting",

                'font': {
                    'color': colors['text'],
                    'family':"Courier New, monospace",
                    'size':18,
                    'textAlign': 'left',
                }


            }
        }
    ),
    dash_table.DataTable(
        data=test_case.to_dict('records') + test_case_today.to_dict('records'),
        columns=[{'id': c, 'name': c} for c in test_case.columns],

        style_as_list_view=True,
        style_header={'backgroundColor': 'rgb(30, 30, 30)',
                      'fontWeight': 'bold',
                      'textAlign': 'center',
                      'color': 'white',
                      'font-family': 'Times New Roman',
                      'fontSize': 20

                      },

        style_cell={
            'backgroundColor': 'rgb(50, 50, 50)',
            'textAlign': 'center',
            'color': 'white',
            'fontWeight': 'bold',
            'font-family': 'Times New Roman',
            'fontSize': 20,
            'marginBottom': '10px'

        },
    ),
    dcc.Graph(figure=fig),
    dcc.Graph(figure=fig_stack),
    html.H2(children='LATEST COVID-19 HOTSPOTS IN KERALA[UPDATED]', style={
        'textAlign': 'center',
        'color': colors['text']
    }),
    html.Iframe(id='map', srcDoc = open('map.html','r').read(), width='100%',height='600'),
   
    dcc.Graph(
        id='Graph1',
        figure={
            'data': [
                {'x': date, 'y': postivecase, 'type': 'line', 'name': 'Postive Cases',},
                
              
                
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
    dash_table.DataTable(
        data=test_report.to_dict('records'),
        columns=[{'id': c, 'name': c} for c in test_report.columns],

        style_as_list_view=True,
        style_header={'backgroundColor': 'rgb(30, 30, 30)',
                      'fontWeight': 'bold',
                      'textAlign': 'center',
                      'color': 'white',
                      'font-family': 'Times New Roman',
                      'fontSize': 20

                      },

        style_cell={
            'backgroundColor': 'rgb(50, 50, 50)',
            'textAlign': 'center',
            'color': 'white',
            'fontWeight': 'bold',
            'font-family': 'Times New Roman',
            'fontSize': 20,
            'marginBottom': '10px'

        },
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
