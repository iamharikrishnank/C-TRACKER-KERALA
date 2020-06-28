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
    new_value= value.split(sep, 1)[0] + ',Kerala'
    list.append(new_value)
from opencage.geocoder import OpenCageGeocode
key = "14329a2c03fc4953a4c1f9b223b21cd4"
 
 
 
geocoder = OpenCageGeocode(key)


list_location=[]
list_lat=[]
list_lng=[]
query = list
for a in query:
 
        results = geocoder.geocode(a)
        for b in results:
    
 
            lat = results[0]['geometry']['lat']
 
            lng = results[0]['geometry']['lng']
        location=[lat,lng]
        
        list_location.append([lat,lng])
map_osm=folium.Map(location=[10.850516,76.271080], zoom_start=7.4, tiles='OpenStreetMap')



for point in range(0,len(list_location)) :
        
      folium.Marker(list_location[point], popup=list[point]).add_to(map_osm)
map_osm.save('map.html')

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1('Covid'),
    



if __name__ == '__main__':
    app.run_server(debug=True)
