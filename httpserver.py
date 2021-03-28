import http.server
import socketserver
import json
import numpy as np
import pickle
from utility.mapData import mapUser
from utility.readCsvFile import readRedTeam

PORT = 12345


def handlePost(classifierSelection="Default", classifierList=[], inputDataSelection="Default", inputDataList=[]):
    classifierFolder="classifier/"
    resultThreshold = 0.5
    voteThreshold = 0.5
    err = None
    result = []

    clfList = []
    maplist = pickle.load(open(classifierFolder+"computerEncodeMapList.sav", "rb"))

    try:
        #load classifier
        if classifierSelection == "Default":
            #dosomething
            defaultClassifier = pickle.load(open(classifierFolder+"DecisionTreeDefault.sav", "rb"))
            clfList.append(defaultClassifier)
        else:
            for classifierName in classifierList:
                clf = pickle.load(open(classifierFolder+transClfName(classifierName), "rb"))
                clfList.append(clf)
    except:
        print("error in loading classifier")
        return result, "error in loading classifier"

    #load data red team or use user input rightaway
    if inputDataSelection =="Default":
        #load Red team data
        testfile="data/redteam.txt"
        dataList, maplist = readRedTeam(testfile, maplist)
        inputDataList = np.array(dataList)[:,:2]
    else:
        templist = []
        templist, maplist = mapData(maplist, inputDataList)
        inputDataList = [templist]
        #print(inputDataList)
    #fit and get result
    try:
        for data in inputDataList:
            tempresult = []

            for clf in clfList:
                r = clf.predict([data])
                #turn result to 0/1
                if r > resultThreshold:
                    tempresult.append(1)
                else:
                    tempresult.append(0)
            print(tempresult)

            #coutFalse
            # if > voteThreshold is 1(failure)
            if tempresult.count(1)/len(tempresult) >= voteThreshold:
                result.append(1)
            else:
                result.append(0)
        #print(result)
    except:
        print("error in predicting result")
        return result, "error in predicting result"

    return result, err

def transClfName(originalName="DecisionTreeDefault"):
    return{
        "DecisionTreeDefault"  :   "DecisionTreeDefault.sav",
        "KNNDefault"           :   "KNNDefault.sav",
        "KNNBestParam"         :   "KNNBestParam.sav",
        "MLPDefault"           :   "MLPDefault.sav",
        "MNBDefault"           :   "MNBDefault.sav",
        "CNBDefault"           :   "CNBDefault.sav",
        "NBDefault"            :   "NBDefault.sav",
        "SVMDefault"           :   "SVMDefault.sav"
    }.get(originalName, "DecisionTreeDefault.sav")

def mapData(maplist=[], data=["C1234", "C2345"]):
    r = []
    for d in data:
        x, maplist = mapUser(d, maplist)
        r.append(x)
    return r, maplist

class serverResponseHandler(http.server.BaseHTTPRequestHandler):
    def setheader(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

    def do_GET(self):
        print("GET request received")
        self.setheader()
        self.wfile.write("<p>GET request received<p>".format(self.path).encode('utf-8'))

    def do_POST(self):
        #sample KNN+CNB+NB+MNB, C456+C789 will return [1]
        print("POST request received")
        len = int(self.headers['Content-Length'])
        postData = self.rfile.read(len)
        print(str(postData.decode('utf8')))
        jsonData = json.loads(postData)
        print(jsonData)
        print("classifierSelection:" + jsonData["classifierSelection"])
        print("classifierList:" + str(jsonData["classifierList"]))
        print("inputDataSelection" + jsonData["inputDataSelection"])
        print("inputDataList" + str(jsonData["inputDataList"]))
        defaultClassifier = pickle.load(open("classifier/DecisionTreeDefault.sav", "rb"))

        r, e = handlePost(jsonData["classifierSelection"], jsonData["classifierList"], jsonData["inputDataSelection"], jsonData["inputDataList"])
        self.setheader()
        print("Result String:"+str(r))
        print("Error String:"+str(e))
        if (e is None):
            #TODO: send back JSON code
            #self.wfile.write(json.dumps(r.encode('utf-8')))
            self.wfile.write(json.dumps(r).encode())
        else:
            self.wfile.write(json.dumps(e).encode())

with socketserver.TCPServer(("", PORT), serverResponseHandler) as httpd:
    print("serving at port", PORT)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

    httpd.server_close()
    print("server stopped")
