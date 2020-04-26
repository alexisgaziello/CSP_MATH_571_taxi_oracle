import os
import pandas
from geopandas import GeoDataFrame
import shapely
import matplotlib. pyplot as plt
import numpy as np
from io import BytesIO
from base64 import b64encode

# Load coordinates
def loadCommunities(taxiTrips=None):
    path = os.path.realpath(__file__)

    if os.name == 'nt':
        while path[-1] != '\\':
            path = path[:-2]
    
    elif os.name == 'posix':
        while path[-1] != '/':
            path = path[:-2]
    
    else:
        print(f'What is this OS? {os.name}')

    communities = pandas.read_csv(path + "CommAreas.csv", header=0)
    
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

def updateTaxiTrips(communities, taxiTrips, **kwargs):
    for i in range(0,len(communities)):
        communities.loc[communities.AREA_NUMBE == i+1, 'TAXI_TRIPS'] = taxiTrips[i]

    return showGraph(communities, **kwargs)


def showGraph(communities, showTaxiTrips=True, saveFig='', cmap = 2, figsize=(18,18), saveByte=False, legend=False):
    # Color stuff
    if cmap == 0:
        cmap = "OrRd"
    elif cmap == 1:
        cmap = "YlGn"
    elif cmap == 2:
        cmap = "seismic"
    elif cmap == 3:
        cmap =  "Greys"

    if saveByte:
        plt.switch_backend('Agg')
    elif plt.get_backend() == 'Agg':
        try:
            plt.switch_backend('TkAgg')
        except:
            try:
                plt.switch_backend('WX')
            except:
                try:
                    plt.switch_backend('QTAgg')
                except:
                    print("Error with backend")
    
    # FIGURE SIZE
    fig, ax = plt.subplots(1, 1, figsize=figsize)
    communities.plot(column='TAXI_TRIPS', ax=ax, legend=legend, cmap=cmap)

    # Add text with qty of taxi trips
    if showTaxiTrips:
        for idx, row in communities.iterrows():
            plt.annotate(s= f"{row['TAXI_TRIPS']}"#f"{row['AREA_NUMBE']}={row['TAXI_TRIPS']}"
                , xy=row['CENTER']
                , horizontalalignment='center'
                , backgroundcolor = 'white'
                )

    if saveFig != '':
        print(f"Saving figure to: {saveFig}")
        plt.savefig(saveFig)

    elif saveByte:
        figfile = BytesIO()
        plt.savefig(figfile, format='png')
        figfile.seek(0)
        figdata_png = b64encode(figfile.getvalue())
        figdata_png= str(figdata_png)[2:-1]
        return figdata_png

    else:
        plt.show()


def mapGenerator(taxiTrips, communities = None, **kwargs):
    
    if type(taxiTrips) is dict:
        array = []
        counter = 1
        while(len(array) < 77):
            # Check if value exists
            if counter in taxiTrips:
                array += [taxiTrips[counter]]
            else:
                array += [0]
            
            counter += 1
        taxiTrips = array


    if communities is None:
        communities = loadCommunities()

    # Check if there is one map to generate or several
    typeOfArg = type(taxiTrips[0])
    if (typeOfArg == int or typeOfArg == np.int64):
        return updateTaxiTrips(communities, taxiTrips, **kwargs)

    else:
        for taxiTripsMap in taxiTrips:
            return updateTaxiTrips(communities, taxiTripsMap, **kwargs)


if __name__ == "__main__":
    taxiTrips = np.random.randint(1,50,77)    
    mapGenerator(taxiTrips)
