import folium

# global tooltip
tooltip = 'Click for more info'

# create custom maker icon
logoIcon = folium.features.CustomIcon('Maej.jpg', icon_size=[50, 50])

# create the map object
m = folium.Map(location=[8.460555, -11.779889])

# # create marker
# folium.Marker([42.363600, -71.099500], 
#                 popup='<strong>Location one</strong>',
#                 tooltip=tooltip).add_to(m),

# # create marker
# folium.Marker([42.333600, -71.109500], 
#                 popup='<strong>Location two</strong>',
#                 tooltip=tooltip,
#                 icon=folium.Icon(icon='cloud')).add_to(m),
# # create marker
# folium.Marker([42.375140, -71.032450], 
#                 popup='<strong>Location three</strong>',
#                 tooltip=tooltip,
#                 icon=logoIcon).add_to(m)

# Generate map
m.save('templates/testmap.html')
