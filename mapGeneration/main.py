import pandas
from geopandas import GeoDataFrame
import shapely
import matplotlib. pyplot as plt
import numpy as np

# Load coordinates
def loadCommunities(taxiTrips=None):
    communities = pandas.read_csv("CommAreas.csv", header=0)
    
    communities["TAXI_TRIPS"] = 0

    if(taxiTrips is not None):
        for i in range(0,len(communities)):
            communities.loc[communities.AREA_NUMBE == i+1, 'TAXI_TRIPS'] = taxiTrips[i]

    geometries = []

    for i in range(0,len(communities)):
        geometries.append(shapely.wkt.loads(communities['the_geom'][i]))

    communities = GeoDataFrame(communities, geometry=geometries)

    # Add coordinates for the geometric center of the polygon
    # Representative point
    communities['CENTER'] = communities['geometry'].apply(lambda x: x.representative_point().coords[:])
    communities['CENTER'] = [CENTER[0] for CENTER in communities['CENTER']]

    # Polylabel
    # communities["CENTER"] = None
    # for i in range(0,len(communities)):
    #     if type(communities['geometry'][i]) == shapely.geometry.multipolygon.MultiPolygon:
    #         polygon = max(communities['geometry'][i], key = lambda x: x.area)
    #     else:
    #         polygon = communities['geometry'][i]

    #     communities['CENTER'][i] = shapely.ops.polylabel(polygon, tolerance=10).coords[:]
    
    # communities['CENTER'] = [CENTER[0] for CENTER in communities['CENTER']]


    return communities

def updateTaxiTrips(communities, taxiTrips, saveFig=True):

    for i in range(0,len(communities)):
        communities.loc[communities.AREA_NUMBE == i+1, 'TAXI_TRIPS'] = taxiTrips[i]

    showGraph(communities, saveFig=saveFig)

def showGraph(communities, showTaxiTrips=True, saveFig=True, cmap = 2):
    # Color stuff
    if cmap == 0:
        cmap = "OrRd"
    elif cmap == 1:
        cmap = "YlGn"
    elif cmap == 2:
        cmap = "seismic"
    elif cmap == 3:
        cmap =  "Greys"
    else:
        cmap = "BuPu"

    fig, ax = plt.subplots(1, 1)
    communities.plot(column='TAXI_TRIPS', ax=ax, legend=True, cmap=cmap)

    if showTaxiTrips:
        for idx, row in communities.iterrows():
            plt.annotate(s=row['TAXI_TRIPS'],
                xy=row['CENTER'], horizontalalignment='center')

    if saveFig:
        print("\n\nERROR: SPECIFIY PATH BEFORE TRYING TO SAVE\n\n")
        return 
        plt.savefig("PATH")
    else:
        plt.show()


def mapGenerator(taxiTrips):
    communities = loadCommunities()

    # Check if there is one map to generate or several
    typeOfArg = type(taxiTrips[0])
    if (typeOfArg == int or typeOfArg == np.int64):
        updateTaxiTrips(communities, taxiTrips, saveFig=False)

    else:
        for taxiTripsMap in taxiTrips:
            updateTaxiTrips(communities, taxiTripsMap, saveFig=False)


if __name__ == "__main__":
    taxiTrips = np.random.randint(1,50,77)    
    mapGenerator(taxiTrips)
