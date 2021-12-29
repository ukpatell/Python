import folium
import pandas

data = pandas.read_csv("Volcanoes.txt")
# Import data file using pandas library in data object

lat  = list(data["LAT"])
lon  = list(data["LON"])
elev = list(data["ELEV"])
# convert data txt in list format for easy access

def color_changer(elevation):
    if elevation < 1000:
        return 'green'
    elif 1000 <= elevation < 3000:
        return 'orange'
    else:
        return 'red'

map = folium.Map(location=[40.26, -76.88], zoom_start=4, tiles="Stamen Terrain")

fgVolcanoes = folium.FeatureGroup(name="Volcanoes")

# Loop iterates a list of co_ordinates
for lt,ln,el in zip(lat,lon,elev):
    fgVolcanoes.add_child(folium.CircleMarker(location=[lt,ln], popup = str(el) + " m",
    fill_color = color_changer(el), color = 'blue', fill_opacity = 0.7))

# NOTE: Unsure why el = default is float but it still run, without converting to string as expectation
# Run: help(folium) --> a
# You can also add multiple markers by using line 9 multiple times or using a Loop
# In here, we have used zip to iterate loop at the same time from the imported file

fgPopulation = folium.FeatureGroup(name="Population")

fgPopulation.add_child(folium.GeoJson(data=open('world.json','r',# -*- coding: utf-8 -*-
encoding='utf-8-sig').read(),style_function=lambda x: {'fillColor':'green' if x['properties']['POP2005'] < 10000000
else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'}))
# Population Layer


map.add_child(fgVolcanoes)
map.add_child(fgPopulation)
map.add_child(folium.LayerControl())
# Layer Control should be last

map.save("Map1.html")
