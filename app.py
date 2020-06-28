import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import requests
import folium
url = 'https://keralastats.coronasafe.live/hotspots.json'
r = requests.get(url)
x = r.json()
df=pd.DataFrame(x['hotspots'])
data=df.lsgd

list=[]
for i in range (0,len(data)):
    sep = ' '
    value = data[i]
    dist = df.district[i]
    new_value= value.split(sep, 1)[0] + ',' + dist.split(sep, 1)[0] + ',Kerala' + ',India'
    list.append(new_value)
list_location=[]
URL = "https://geocode.search.hereapi.com/v1/geocode"

for a in list:
    location = a #taking user input
    api_key = 'MeIrhhrqJ0h9LaQ7euxAaRPCUokDr_7N0KUVYHd0O0M' # Acquire from developer.here.com
    PARAMS = {'apikey':api_key,'q':location} 

    # sending get request and saving the response as response object 
    r = requests.get(url = URL, params = PARAMS) 
    data = r.json()

    latitude = data['items'][0]['position']['lat']
    longitude = data['items'][0]['position']['lng']
    print(latitude,longitude)
    list_location.append([latitude,longitude])

map_osm=folium.Map(location=[10.850516,76.271080], zoom_start=7.4, tiles='OpenStreetMap')
for point in range(1,len(list_location)) :
        
      folium.Marker(list_location[point], popup=list[point]).add_to(map_osm)



map_osm.save('map.html')


app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1('Covid'),
    html.Iframe(id='map', srcDoc = open('map.html','r').read(), width='100%',height='600')])



if __name__ == '__main__':
    app.run_server(debug=True)
