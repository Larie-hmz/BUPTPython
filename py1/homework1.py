from sanic import Sanic
from sanic import response
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

app = Sanic(__name__)

data_path=f'{dir_path}/test.txt'
@app.listener('before_server_start')
async def load_file(app,loop):   #协程关键词
    app.config.myDict=dict()
    #await asyncio.sleep(0.001)

    with open(data_path) as f:
        for line in f.readlines():
            words=line.split()
            if len(words)<3 or words[0].startswith('#'):  #数据清洗
                continue
            year= words[0]
            app.config.myDict[year]=(words[1],words[2])

@app.middleware('request')
async def checkArg(req):
    startYear=req.args.get('start',int(1880))
    endYear = req.args.get('end',int(2020))  
    req.ctx.resultsDict = dict()
    for k,v in app.config.myDict.items():
        if startYear <=k and k<=endYear:
            req.ctx.resultsDict[k]=(v[0],v[1])

@app.get("/csv")
async def root(req):
    results = list()
    for k,v in req.ctx.resultsDict.items():
        results.append(f'{k},{v[0]},{v[1]}')

    return response.text('\n'.join(results))

@app.get("/json")
async def root(req):
    return response.json(req.ctx.resultsDict)

if __name__=="__main__":
    app.run(host='0.0.0.0',port=8000)