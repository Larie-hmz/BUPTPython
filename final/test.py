from re import split
import numpy as np
import pandas as pd
import struct
from shapely import geometry

def calcPopulation(lonLats):
    polygon = geometry.Polygon(lonLats)
    lonMin,latMin,lonMax,latMax = polygon.bounds
    step = 30 / 3600 #步长为30角秒，转换为角度
    cellArea = geometry.box(0,0,step,step).area
    populationTotal = 0
    for lon in np.arange(lonMin,lonMax,step):
        for lat in np.arange(latMin,latMax,step):
            cellLon1 = lon - lon % step - step
            cellLon2 = lon - lon % step + step
            cellLat1 = lat - lat % step - step
            cellLat2 = lat - lat % step + step
            cellPolygon = geometry.box(cellLon1,cellLat1,cellLon2,cellLat2)
            area = cellPolygon.intersection(polygon).area
            if(area > 0.0):
                p = 0.5
                populationTotal += (area/cellArea) *p
    return populationTotal

x=calcPopulation([(0.1,0.05),(0.2,0.2),(0.3,0.2),(0.3,0.1),(0.1,0)])
print(f'x={x}')