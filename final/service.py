from os import get_terminal_size
from re import split
import numpy as np
import struct
from shapely import geometry
from sanic import Sanic
from sanic import response
from sanic.response import json


app = Sanic("__name__")

grids=list()

@app.route("/search/<lons>/<lats>")
async def search(req,lons,lats):
    lon=lons.split(",")
    lat=lats.split(",")
    lonLate=[]
    for i in range(len(lon)):
        lonLate.append((float(lon[i]),float(lat[i])))

    print(lonLate)
    popTotal=calcPopulation(lonLate)

    # grids.append({"populationTotal":popTotal})

    return json(grids)

#从文件中读取面积
def getPopulationFromFile(lon,lat):
    #每一个面积占用4位
    cellsize = 30 / 3600
    sizeoffset=10800
    blockoffset=116640000
    blocknum=0
    floatoffset=4
    x=0
    y=0
    if(lon>=-180 and lon<90 and lat>=-4.2632564145606e-14):
        blocknum=0
        x = int((lon-(-180))/cellsize)
        y = int((90-lat)/cellsize)
    elif(lon>=-90 and lon<-8.5265128291212e-14 and lat>=-4.2632564145606e-14):
        blocknum=1
        x = int((lon-(-90))/cellsize)
        y = int((90-lat)/cellsize)
    elif(lon>=-8.5265128291212e-14 and lon<90 and lat>=-4.2632564145606e-14): 
        blocknum=2
        x = int((lon-(-8.5265128291212e-14))/cellsize)
        y = int((90-lat)/cellsize)
    elif(lon>=90 and lat>=-4.2632564145606e-14):
        blocknum=3
        x = int((lon-(90))/cellsize)
        y = int((90-lat)/cellsize) 
    elif(lon>=-180 and lon<90):
        blocknum=4
        x = int((lon-(-180))/cellsize)
        y = int((-4.2632564145606e-14-lat)/cellsize)  
    elif(lon>=-90 and lon<-8.5265128291212e-14):
        blocknum=5
        x = int((lon-(-90))/cellsize)
        y = int((-4.2632564145606e-14-lat)/cellsize)
    elif(lon>=-8.5265128291212e-14 and lon<90):
        blocknum=6
        x = int((lon-(-8.5265128291212e-14))/cellsize)
        y = int((-4.2632564145606e-14-lat)/cellsize)
    elif(lon>=90):
        blocknum=7
        x = int((lon-(-180))/cellsize)
        y = int((-4.2632564145606e-14-lat)/cellsize)    
    else:
        print("error！")


    with open("predata.bin","rb") as fin:
        fin.seek((blockoffset*blocknum+y*sizeoffset+x)*floatoffset)
        (data,)=struct.unpack('f',fin.read(floatoffset))   
        #print(blockoffset,x,y)         

    if(data-(-9999.0)<=1e-6):
        return 0
    return data

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
                p = getPopulationFromFile(cellLon1,cellLat1)
                print(p)
                populationTotal += (area/cellArea) *p
                grids.append({'longitude':lon,'latitude':lat,'population':p})

    return populationTotal


#数据预处理
def preDealdata():
    with open("predata.bin","wb") as fw:
        for i in range(1,9):
            count=0
            fname=f'F:/zzz/作业/python/final/data/gpw_v4_population_count_rev11_2020_30_sec_{i}.asc'
            with open(fname) as fr:
                for line in fr.readlines():  
                    if(count<6):
                        count=count+1
                        continue
                    for j in line.split():
                        #print (float(j))
                        data=struct.pack('f',float(j))
                        fw.write(data)    


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8080)