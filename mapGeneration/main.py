import pandas
from geopandas import GeoDataFrame
import shapely.wkt
import matplotlib. pyplot as plt
import numpy as np

# Load coordinates
def loadCommunities(taxiTrips):
    communities = pandas.read_csv("CommAreas.csv", header=0)
    
    communities["TAXI_TRIPS"] = 0

    for i in range(0,len(communities)):
        communities.loc[communities.AREA_NUMBE == i+1, 'TAXI_TRIPS'] = taxiTrips[i]

    geometries = []

    for i in range(0,len(communities)):
        #communities['geometry'][i] = shapely.wkt.loads(communities['the_geom'][i])
        geometries.append(shapely.wkt.loads(communities['the_geom'][i]))

    communities = GeoDataFrame(communities, geometry=geometries)
    return communities


if __name__ == "__main__":
    taxiTrips = np.random.randint(1,50,77)
    communities = loadCommunities(taxiTrips)

    fig, ax = plt.subplots(1, 1)

    communities.plot(column='TAXI_TRIPS', ax=ax, legend=True)
    

    plt.show()
