from sanic import Sanic
from sanic import response
from sanic.response import json
import copy
from xml.dom.minidom import Document

app = Sanic("__name__")
  
temper=[]
tempi=[]
tempd=[]
name=["year","Land-Ocean Temperature Index","Year No_Smoothing  Lowess"]
def read_files():
    fo=open("F:/zzz/AllCode/python/prj/test.txt","r")
    #以列表方式存储
    for line in fo:
        a, b, c = [float(i) for i in line.split()]
        #print(a,b,c)
        temper.append([int(a),b,c])
    fo.close()

def takeSecond(elem):
    return elem[1]

@app.route("/json/increase")
async def post_json(request):
    tempi=copy.deepcopy(temper)
    tempi.sort(key=takeSecond)
    tempans=list()
    for words in tempi:
        tempans.append({'year':words[0],'temperature':words[1],'lowess':words[2]})
    return json(tempans)

@app.route("/xml/increase")
async def post_json(request):
    tempi=copy.deepcopy(temper)
    tempi.sort(key=takeSecond)
    # 创建doc
    doc = Document()
    # 创建根节点
    root_node = doc.createElement("all_data")  
    doc.appendChild(root_node)  
    for list in tempi:
        data_node = doc.createElement("data") 
        year_node = doc.createElement("year")  
        year_value = doc.createTextNode(str(list[0]))  
        year_node.appendChild(year_value)  
        data_node.appendChild(year_node)  
        year_node = doc.createElement("Temperature")
        year_value = doc.createTextNode(str(list[1])) 
        year_node.appendChild(year_value)  
        data_node.appendChild(year_node)  
        year_node = doc.createElement("Lowess")
        year_value = doc.createTextNode(str(list[2])) 
        year_node.appendChild(year_value)  
        data_node.appendChild(year_node)  
        root_node.appendChild(data_node)  

    with open('F:/zzz/AllCode/python/prj/note.xml', 'w') as f:
        f.write(doc.toprettyxml(indent='\t'))
    return await response.file('F:/zzz/AllCode/python/prj/note.xml')

@app.route("/csv/increase")
async def post_json(request):
    tempi=copy.deepcopy(temper)
    tempi.sort(key=takeSecond) 
    with open("F:/zzz/AllCode/python/prj/test2.txt","w") as f:
        for list in tempi:
            s=str(list[0])+","+str(list[1])+","+str(list[2])+"\n"
            f.write(s) 
    return await response.file('F:/zzz/AllCode/python/prj/test2.txt')

@app.route("/json/decrease")
async def post_json(request):
    tempd=copy.deepcopy(temper)
    tempd.sort(key=takeSecond,reverse=True)
    tempans=list()
    for words in tempd:
        tempans.append({'year':words[0],'temperature':words[1],'lowess':words[2]})
    return json(tempans)

@app.route("/xml/decrease")
async def post_json(request):
    tempd=copy.deepcopy(temper)
    tempd.sort(key=takeSecond,reverse=True)
    # 创建doc
    doc = Document()
    # 创建根节点
    root_node = doc.createElement("all_data")  
    doc.appendChild(root_node)  
    for list in tempd:
        data_node = doc.createElement("data") 
        year_node = doc.createElement("year")  
        year_value = doc.createTextNode(str(list[0]))  
        year_node.appendChild(year_value)  
        data_node.appendChild(year_node)  
        year_node = doc.createElement("Temperature")
        year_value = doc.createTextNode(str(list[1])) 
        year_node.appendChild(year_value)  
        data_node.appendChild(year_node)  
        year_node = doc.createElement("Lowess")
        year_value = doc.createTextNode(str(list[2])) 
        year_node.appendChild(year_value)  
        data_node.appendChild(year_node)  
        root_node.appendChild(data_node)  

    with open('F:/zzz/AllCode/python/prj/note.xml', 'w') as f:
        f.write(doc.toprettyxml(indent='\t'))
    return await response.file('F:/zzz/AllCode/python/prj/note.xml')

@app.route("/csv/decrease")
async def post_json(request):
    tempd=copy.deepcopy(temper)
    tempd.sort(key=takeSecond,reverse=True)
    with open("F:/zzz/AllCode/python/prj/test2.txt","w") as f:
        for list in tempd:
            s=str(list[0])+","+str(list[1])+","+str(list[2])+"\n"
            f.write(s) 
    return await response.file('F:/zzz/AllCode/python/prj/test2.txt')

@app.route('/json/start/<start:int>/end/<end:int>')
async def query_year(request,start,end):
    tempans=list()
    for words in temper[start-1880:end-1880+1]:
        tempans.append({'year':words[0],'temperature':words[1],'lowess':words[2]})
    return json(tempans)



@app.route('/xml/start/<start:int>/end/<end:int>')
async def query_year(request,start,end):
    # 创建doc
    doc = Document()
    # 创建根节点
    root_node = doc.createElement("all_data")  
    doc.appendChild(root_node)  
    for list in temper[start-1880:end-1880+1]:
        data_node = doc.createElement("data") 
        year_node = doc.createElement("year")  
        year_value = doc.createTextNode(str(list[0]))  
        year_node.appendChild(year_value)  
        data_node.appendChild(year_node)  
        year_node = doc.createElement("Temperature")
        year_value = doc.createTextNode(str(list[1])) 
        year_node.appendChild(year_value)  
        data_node.appendChild(year_node)  
        year_node = doc.createElement("Lowess")
        year_value = doc.createTextNode(str(list[2])) 
        year_node.appendChild(year_value)  
        data_node.appendChild(year_node)  
        root_node.appendChild(data_node)  

    with open('F:/zzz/AllCode/python/prj/note.xml', 'w') as f:
        f.write(doc.toprettyxml(indent='\t'))
    return await response.file('F:/zzz/AllCode/python/prj/note.xml')

@app.route('/csv/start/<start:int>/end/<end:int>')
async def query_year(request,start,end):
    with open("F:/zzz/AllCode/python/prj/test2.txt","w") as f:
        for list in temper[start-1880:end-1880+1]:
            s=str(list[0])+","+str(list[1])+","+str(list[2])+"\n"
            f.write(s) 
    return await response.file('F:/zzz/AllCode/python/prj/test2.txt')

if __name__=="__main__":
    read_files()
    app.run(host="0.0.0.0",port=8000)


