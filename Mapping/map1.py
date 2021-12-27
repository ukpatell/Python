import folium
import pandas

data = pandas.read_csv("Volcanoes.txt")
# Import data file using pandas library in data object

lat  = list(data["LAT"])
lon  = list(data["LON"])
elev = list(data["ELEV"])
# convert data txt in list format for easy access

map = folium.Map(location=[40.26, -76.88], zoom_start=4, tiles="Stamen Terrain")

fg = folium.FeatureGroup(name="My Map")

# Loop iterates a list of co_ordinates
for lt,ln,el in zip(lat,lon,elev):
    fg.add_child(folium.Marker(location=[lt,ln], popup = el, icon=folium.Icon(color='green')))
# NOTE: Unsure why el = default is float but it still run, without converting to string as expectation
# Run: help(folium) --> a
# You can also add multiple markers by using line 9 multiple times or using a Loop
# In here, we have used zip to iterate loop at the same time from the imported file

map.add_child(fg)


map.save("Map1.html")
