import folium
import pandas as pd
import os

districts = os.path.join('data', 'salone_geo.json')
water_stations_data = os.path.join('data', 'water_stations.csv')

districts_data = pd.read_csv(water_stations_data)

ma = folium.Map(location=[8.460555, -11.779889], zoom_start=3)

folium.Choropleth(
    geo_data=districts,
    name='choropleth',
    data=districts_data,
    columns=['Latitude','Longitude'],
    fill_color='YlGn',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Water Stations'
)

folium.LayerControl().add_to(ma)

ma.save('templates/salone-map.html')

