This toolbox has been created in order to construct from scratch a METROPOLIS' simulation using OpenStreetMaps data.  
It includes a script to construct connectors, a script to construct zones file. 
In addition, you can also find a script to downscale OD matrix to an higher resolution and also a script to transform METROPOLIS' inputs into shapefile. 

Notice, that first you have to follow this tutorial in order to create the needed files from OpenStreetMaps : https://metropolis.sauder.ubc.ca/osm_tutorial

More information on the methodologies used by those script could be find in the technical_notes.pdf file

## create_zones.py

This script allows its users to create create zones centroid csv file that could be used in a METROPOLIS' simulation. Notice that in order to run this script you should download before a shapefile (.shp) of all the zones.  

It takes the following inputs, with the following default values, those can be modified in the inputs section of the script:

  - zone_shapefile_path : The path to the shapefile of the zone
  - OD_matrix : The path to the OD matrix csv file
  - output_path = ".../zones.csv" : The path to the outputs csv file

## create_connectors.py 

This script allows its users to create connectors csv file that could be used in a METROPOLIS' simulation. 

It takes the following inputs, with the following default values, those can be modified in the inputs section of the script:

  - intersections_path : The path to the intersections csv file produced with the OpenStreetMaps script 
  - zones_path : The path to the zones csv file produced with the create_zones.py script 
  - links_path : The path to the links csv file produced with the OpenStreetMaps script
  - output_path = ".../links_connectors.csv" : The path to the outputs csv file.
  - max_speed_connection = 129 : It is the maximum of links to which connectors can be connected
  - min_capacity_connection = 1001 : It is the minimum capacity of links to which the connectors can be connected
  - among_closest = 15 : It is the number of closest intersection to which the connectors can be created
  - connectors_parameters = {"function" : 1, "lanes" : 5, "speed" : 200, "capacity" : 99999} : It is the general parameters for the connectors
    - function = 1 : It is the congestion function default value is set to FreeFlow
    - lanes = 5 : It is number of lanes for each connector
    - speed = 200 : is the speed on each connectors 
    - capacity = 99999 : is the capacity of each lane for each connector
    
    Notice that those default values are set in order to do not create any congestion
    
## METRO_to_shapefile.py 

This script allows its users to create connectors csv file that could be used in a METROPOLIS' simulation. 

It takes the following inputs, with the following default values, those can be modified in the inputs section of the script:

  - intersections_path : The path to the intersections csv file
  - links_path : The path to the links csv file
  - output_path = ".../network.shp" : The path to the output shapefile.

## rescale_OD_matrix.py

This script allows its users to rescall and export in a csv file an OD matrix that could be used in a METROPOLIS' simulation. 

It takes the following inputs, with the following default values, those can be modified in the inputs section of the script:

  - zone_shapefile_path : The path to the shapefile of the zone
  - path_OD_matrix : The path to the original OD matrix csv file
  - output_path = ".../rescalled_OD_matrix.csv" : The path to the output csv file
    
    This file must includes for each zone 2 columns one with an identifier of the old zone and one identifier for the new zone

  - population_tiff_path : The path to the tiff file of population count
  - residential_tiff_path : The path to the tiff file of residential building density
  - working_tiff_path : The path to the tiff file of working building density 
  - road_tiff_path : The path to the tiff file of road length density
  
    This file has to be downloaded or produced using external sources (example: Qgis...) 

  - diag_scaling_factor = 0 : This scalling factor is used to reduce the size of the population of the diagonal of the original OD matrix 
  - column_name_old_zone : This is the name of the column in which the ID/name of the old zone are stored in the zone shapefile
  - columns_name_new_zone : This is the name of the column in which the ID/name of the new zone are stored in the zone shapefile

    
