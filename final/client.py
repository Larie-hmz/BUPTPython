import aiohttp
import asyncio
import argparse
import json
import matplotlib.pyplot as pl
import numpy as np


async def main(host,port,longitude,latitude):
    url=f'http://{host}:{port}/search/{longitude}/{latitude}'
    async with aiohttp.ClientSession(trust_env=True) as session:
        async with session.get(url,verify_ssl=False) as response:
            print("Status:", response.status)
            print("Content-type:", response.headers['content-type'])
            text = await response.text()
            temper=list()
            temper=json.loads(text)

            xList = list()
            yList = list()
            zList = list()
            for item in temper:
                xList.append(item['longitude'])
                yList.append(item['latitude'])
                zList.append(item['population'])
            x=np.array(xList)
            y=np.array(yList)
            z=np.array(zList)

            pl.clf()
            pl.grid()
            pl.scatter(x,y,c=z,vmin=0,vmax=8000,cmap='RdYlGn_r')
            pl.colorbar()
            pl.legend()
            pl.show()
            


if __name__=='__main__':
    parser = argparse.ArgumentParser(description='world temperature')
    parser.add_argument('--longitude',dest='longitude',default='115,115,116,117,117')
    parser.add_argument('--latitude',dest='latitude',default='38,39,40,39,38.2')
    parser.add_argument('host')
    parser.add_argument('port')
    args=parser.parse_args()
    print(f'{args}')

    asyncio.run(main(args.host,args.port,args.longitude,args.latitude))