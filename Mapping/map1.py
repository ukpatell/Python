import folium

map = folium.Map(location=[40.26, -76.88], zoom_start=4, tiles="Stamen Terrain")

fg = folium.FeatureGroup(name="My Map")

for co_ordinates in [[40.26,-76.88],[40.40,-95]]:
    fg.add_child(folium.Marker(location=co_ordinates, popup = "Marker", icon=folium.Icon(color='green')))
# You can also add multiple markers by using line #6

map.add_child(fg)


map.save("Map1.html")
