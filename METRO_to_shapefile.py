mport pandas as pd
import geopandas as gpd 
from shapely.geometry.polygon import LineString

############
## INPUTS ##
############

intersections_path = "D:/.../.csv"
links_path = "D:/.../.csv
output_path = "D:/.../network.shp"

############
## SCRIPT ##
############

print("Load inputs...")

df_links = pd.read_csv(links_path)
df_intersections = pd.read_csv(intersections_path)
df_intersections = df_intersections[["id", "x", "y"]]


print("Create the GeoDataFrame...")

ids = []
geometry = []
functions = []
lanes = []
speed = []
length = []
capacity = []
origin = []
destination = []

for _, l in df_links.iterrows():
    x_destination = df_intersections[df_intersections["id"] == l["destination"]]["x"] 
    y_destination = df_intersections[df_intersections["id"] == l["destination"]]["y"]
    x_origin = df_intersections[df_intersections["id"] == l["origin"]]["x"] 
    y_origin = df_intersections[df_intersections["id"] == l["origin"]]["y"]
    poly = LineString([(x_destination, y_destination), (x_origin, y_origin)])
    ids.append(int(l["id"]))
    functions.append(int(l["function"]))
    lanes.append(int(l["lanes"]))
    speed.append(int(l["speed"]))
    length.append(float(l["length"]))
    capacity.append(int(l["capacity"]))
    origin.append(int(l["origin"]))
    destination.append(int(l["destination"]))
    geometry.append(poly)
    
print("Save the data in a shapefile...")

df = pd.DataFrame(list(zip(ids, functions, lanes, speed, length, capacity, origin, destination)), columns=['id', 'function', 'lanes', 'speed', 'length', 'capacity', 'origin', 'destination'])
gdf = gpd.GeoDataFrame(df, geometry=geometry)

gdf.to_file(output_path, index=False)    

