import aiohttp
import asyncio
import argparse
import json
import xml.etree.ElementTree as xmlet

async def main(host,port,start,end,fmt):
    url=f'http://{host}:{port}/{fmt}/start/{start}/end/{end}'
    async with aiohttp.ClientSession(trust_env=True) as session:
        async with session.get(url,verify_ssl=False) as response:
            print("Status:", response.status)
            print("Content-type:", response.headers['content-type'])
            text = await response.text()
            temper=list()
            if fmt=='csv':
                lines=text.split('\n')
                for line in lines:
                    if line=="":
                        continue
                    words=line.split(',')
                    temper.append({'year':words[0],'temperature':words[1],'lowess':words[2]})

            elif fmt=='xml':
                root=xmlet.fromstring(text)
                for child in root:
                    temper.append({'year':child[0].text,'temperature':child[1].text,'lowess':child[2].text})
            elif fmt=='json':
                temper=json.loads(text)
    
            for words in temper:
                print('year:{0} temperature:{1} lowess:{2} '.format(words['year'],words['temperature'],words['lowess']))
            
           

# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='world temperature')
    parser.add_argument('--start',dest='start',type=int,default=1880)
    parser.add_argument('--end',dest='end',type=int,default=2020)
    parser.add_argument('--fmt',dest='fmt',default='json')
    parser.add_argument('host')
    parser.add_argument('port')
    args=parser.parse_args()
    print(f'{args}')

    asyncio.run(main(args.host,args.port,args.start,args.end,args.fmt))


