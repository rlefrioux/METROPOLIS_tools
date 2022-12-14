import pandas as pd
import geopandas as gpd

 ############
 ## INPUTS ##
 ############
 
zone_shapefile_path = ".../.shp"
OD_matrix = ".../.csv"
output_path = ".../zones.csv"

############
## SCRIPT ##
############

#Load files
gdf_iris = gpd.read_file(zone_shapefile_path)
OD_matrix = pd.read_csv(OD_matrix_path)

#Restrict the OD matrix to pairs with positive population
OD_matrix = OD_matrix[OD_matrix["population"] != 0]

#Get the list of origin and destination with positive population
origin_id = OD_matrix["origin"].unique()
destination_id = OD_matrix["destination"].unique()

zone_id = list(set(origin_id) & set(destination_id))

xs = []
ys = []

gdf_iris["centroid"] = gdf_iris["geometry"].centroid

#Create the centroid for each zone
for i in zone_id:
    gdf = gdf_iris[gdf_iris["CODE_IRIS"] == str(i)]    
    centroid = gdf.centroid
    xs.append(centroid.x.mean())    
    ys.append(centroid.y.mean())
    
#Create and save the outputs dataframe    
df = pd.DataFrame(list(zip(zone_id, xs, ys)), columns=["id", "x", "y"])
df.to_csv(output_path)
