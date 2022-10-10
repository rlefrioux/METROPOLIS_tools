This toolbox has been created in order to construct from scratch a METROPOLIS' simulation using OpenStreetMaps data.  
It includes a script to construct connectors, a script to construct zones file. 
In addition, you can also find a script to downscale OD matrix to an higher resolution and also a script to transform METROPOLIS' inputs into shapefile. 

Notice, that first you have to follow this tutorial in order to create the needed files from OpenStreetMaps : https://metropolis.sauder.ubc.ca/osm_tutorial

More information on the methodologies used by those script could be find in the technical_notes.pdf file

## create_zones.py

This script allows its users to create create zones file that could be used in a METROPOLIS' simulation.

## create_connectors.py 

This script allows its users to create create connectors that could be used in a METROPOLIS' simulation. 

It takes the following inputs, with the following default values, those can be modified in the inputs section of the script:

  - intersections_path : The path to the csv intersections file produced with the OpenStreetMaps script 
  - zones_path : The path to the zones csv file produced with the create_zones.py script 
  - links_path : The path to the links csv file produced with the OpenStreetMaps script
  - output_path : The path to the outputs files. The default name of the ouputs file is links_connectors.csv
  - max_speed_connection = 129 : It is the maximum of links to which connectors can be connected
  - min_capacity_connection = 1000 : It is the minimum capacity of links to which the connectors can be connected
  - among_closest = 15 : It is the number of closest intersection to which the connectors can be created
  - connectors_parameters = {"function" : 1, "lanes" : 5, "speed" : 200, "capacity" : 99999} : It is the general parameters for the connectors
    - function = 1 : It is the congestion function default value is set to FreeFlow
    - lanes = 5 : It is number of lanes for each connector
    - speed = 200 : is the speed on each connectors 
    - capacity = 99999 : is the capacity of each lane for each connector
    
    Notice that those default values are set in order to do not create any congestion