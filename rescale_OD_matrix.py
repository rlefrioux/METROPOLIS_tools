import pandas as pd 
import geopandas as gpd
from osgeo import gdal
import numpy as np
from shapely.geometry import Point
import random

def pixel_to_world(geo_matrix, x, y):
    ul_x   = geo_matrix[3]
    ul_y   = geo_matrix[0]
    x_dist = geo_matrix[5]
    y_dist = geo_matrix[1]
    _x = x * x_dist + ul_x
    _y = y * y_dist + ul_y
    return Point(_y, _x)

############
## INPUTS ##
############  

zone_shapefile_path = ".../.shp"
population_tiff_path = ".../.tif"
residential_tiff_path = ".../.tif"
working_tiff_path = ".../.tif"
road_tiff_path = ".../.tif"
path_OD_matrix = ".../.csv"
output_path = ".../rescalled_OD_matrix.csv"
diag_scaling_factor = 0
column_name_old_zone = ""
columns_name_new_zone = ""

############
## SCRIPT ##
############  

gpd_iris = gpd.read_file(zone_shapefile_path)

#COMPLETE GEODDATAFRAME IRIS WITH POPULATION....
#Population

gpd_iris["population"] = 0

tiff_pop = gdal.Open(population_tiff_path)
arr_pop = tiff_pop.ReadAsArray()
geo_matrix = tiff_pop.GetGeoTransform()    
band = tiff_pop.GetRasterBand(1)
arr_pop = np.where(arr_pop == -999, 0, arr_pop)

for x in range(len(arr_pop)):
    for y in range(len(arr_pop[0])):
        if arr_pop[x][y] != 0:
            point = pixel_to_world(geo_matrix=geo_matrix, x=x, y=y)
            for i, r in gpd_iris.iterrows():
                if r["geometry"].contains(point) == True:
                    gpd_iris.at[i, "population"] += arr_pop[x][y]
                    break

#Residential building

gpd_iris["residential"] = 0

tiff_res = gdal.Open(residential_tiff_path)
arr_res = tiff_res.ReadAsArray()
arr_res = arr_res.astype(int)
geo_matrix = tiff_res.GetGeoTransform()    
band = tiff_res.GetRasterBand(1)
arr_res = np.where(arr_res == -999, 0, arr_res)

for x in range(len(arr_res)):
    for y in range(len(arr_res[0])):
        if arr_res[x][y] != 0:
            point = pixel_to_world(geo_matrix=geo_matrix, x=x, y=y)
            for i, r in gpd_iris.iterrows():
                if r["geometry"].contains(point) == True:
                    gpd_iris.at[i, "residential"] += arr_res[x][y]
                    break

#Working building

gpd_iris["working"] = 0

tiff_work = gdal.Open(working_tiff_path)
arr_work = tiff_work.ReadAsArray()
arr_work = arr_work.astype(int)
geo_matrix = tiff_work.GetGeoTransform()    
band = tiff_work.GetRasterBand(1)
arr_work = np.where(arr_work == -999, 0, arr_work)

for x in range(len(arr_work)):
    for y in range(len(arr_work[0])):
        if arr_work[x][y] != 0:
            point = pixel_to_world(geo_matrix=geo_matrix, x=x, y=y)
            for i, r in gpd_iris.iterrows():
                if r["geometry"].contains(point) == True:
                    gpd_iris.at[i, "working"] += arr_work[x][y]
                    break

#Road lenght

gpd_iris["road"] = 0

tiff_road = gdal.Open(road_tiff_path)
arr_road = tiff_road.ReadAsArray()
geo_matrix = tiff_road.GetGeoTransform()    
band = tiff_road.GetRasterBand(1)
arr_road = np.where(arr_road == -999, 0, arr_road)

for x in range(len(arr_road)):
    for y in range(len(arr_road[0])):
        if arr_road[x][y] != 0:
            point = pixel_to_world(geo_matrix=geo_matrix, x=x, y=y)
            for i, r in gpd_iris.iterrows():
                if r["geometry"].contains(point) == True:
                    gpd_iris.at[i, "road"] += arr_road[x][y]
                    break

#Combine
gpd_iris["combine_working"] = gpd_iris["population"]*gpd_iris["working"]*gpd_iris["road"] 
gpd_iris["combine_residential"] = gpd_iris["population"]*gpd_iris["residential"]*gpd_iris["road"] 

#CREATE NEW OD MATRIX USING DENSITY

OD_matrix = pd.read_csv(path_OD_matrix)

commune_list = gpd_iris[column_name_old_zone].unique()
iris_list = gpd_iris[column_name_new_zone].unique()


#Create a dictionnary that store correspondances between municipalities and IRIS zones
commune_to_iris = {}
for m in commune_list:
    commune_to_iris[m] = gpd_iris[gpd_iris[column_name_old_zone] == m][column_name_new_zone].unique()

#Create a dictionnary that store correspondances between IRIS zones and municipalities
iris_to_commune = {}
for i in iris_list:
    iris_to_commune[i] = int(gpd_iris[gpd_iris[column_name_new_zone] == i][column_name_old_zone].mean())


#Create a dictionnary that store total densities for each municipality
mu_population = {}
mu_working = {}
mu_residential = {}
mu_road = {}
mu_combine = {}
mu_combine_work = {}
mu_combine_res = {}

for m in commune_list:
    mu_combine_work[m] = gpd_iris[gpd_iris[column_name_new_zone].isin(commune_to_iris[str(m)])]["combine_working"].sum()
    mu_combine_res[m] = gpd_iris[gpd_iris[column_name_new_zone].isin(commune_to_iris[str(m)])]["combine_residential"].sum()

#Rescall the size of the original OD matrix

for i, r in OD_matrix.iterrows():
    OD_matrix.at[i, str(i)] = r[str(i)]*diag_scaling_factor         


#Create the new number for the OD

destination = []
origin = []
commuters = []

for iris_o in iris_list:
    for iris_d in iris_list:
        destination.append(iris_d)
        origin.append(iris_o)
        commuters_commune = OD_matrix[str(iris_to_commune[str(iris_o)])][int(iris_to_commune[str(iris_d)])]
        weight_o = gpd_iris[gpd_iris[column_name_new_zone]==iris_o]["combine_residential"].mean()/gpd_iris[gpd_iris["INSEE_COM"] == str(iris_to_commune[str(iris_o)])]["combine_residential"].sum()
        weight_d = gpd_iris[gpd_iris[column_name_new_zone]==iris_d]["combine_working"].mean()/gpd_iris[gpd_iris["INSEE_COM"] == str(iris_to_commune[str(iris_d)])]["combine_working"].sum()
        weight = weight_o*weight_d
        if commuters_commune*weight>1:
            commuters.append(round(commuters_commune*weight)+random.randint(0,1))
        else:
            commuters.append(round(commuters_commune*weight))

new_OD_matrix = pd.DataFrame(list(zip(origin, destination, commuters)), columns=["origin", "destination", "population"])

total_diag = 0
for x in iris_list:
    total_diag += new_OD_matrix[(new_OD_matrix["origin"] == x) & (new_OD_matrix["destination"] == x)]["population"].sum()

new_OD_matrix.to_csv(output_path)






