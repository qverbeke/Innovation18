from sklearn.cluster import KMeans
import numpy as np
import elbowCalc as ebc
from scipy.spatial.distance import cdist
import json
from flask import Flask, request
from flask_cors import CORS

data={}
myary=[]
mymodel=[]

class TrainedModel:
    def __init__(self, myary):
        distortions = []
        for k in range(1,10):
            self._kmeans = KMeans(n_clusters=k, random_state=0).fit(myary)
            self._kmeans.fit(myary)
            distortions.append([k,sum(np.min(cdist(myary, self._kmeans.cluster_centers_, 'euclidean'), axis=1))/myary.shape[0]])
        self._k = ebc.get_k(distortions)[0]
        self._kmeans = KMeans(n_clusters=self._k, random_state=0).fit(myary)        
    def classify_point(self, vec):
        return self._kmeans.predict(vec)
    def get_labels(self):
        return self._kmeans.labels_
    
def read_json():
    with open("datastore.json") as f:
        data = json.load(f)
        return data
def write_json():
    with open("datastore.json", "w") as f:
        json.dump(data, f)
def get_ary():
    count = 0
    arylen = 0
    for i in data:
        count+=len(data[i]["vectors"])
        if arylen==0:
            arylen=len(data[i]["vectors"][0])
    result = np.empty(shape=(count, arylen))
    ind = 0
    usrs = []
    for i in data:
        for j in data[i]["vectors"]:
            result[ind] = j
            ind+=1
            usrs.append(i)
    return result,usrs
def handle_new_vec(new_vec, model):
    try:
        tmp_data = new_vec["array"]
        tmp_name = new_vec["name"][0]
        try:
            classification = str(model.classify_point([tmp_data])[0])        
            if(len(data[tmp_name]["vectors"])<5):
                data[tmp_name]["vectors"].append(tmp_data)
                try:
                    data[tmp_name]["class"][classification]+=1
                except(KeyError):
                    data[tmp_name]["class"][classification]=1
            else:
                res = _verify_classification(classification, tmp_name)
                if res:
                   data[tmp_name]["vectors"].append(data)
        except(KeyError):
            data[tmp_name]=_construct_new_entry()
            data[tmp_name]["vectors"].append(tmp_data)
    except(KeyError):
        print("Bad request, ignoring")
        
def _verify_classification(classification, name):
    try:
        total_pts = 0
        for i in data[name]["class"]:
            total_pts+=data[i]
        if data[name]["class"][classification]>=float(total_pts)/10:
            data[name]["class"][classification]+=1
            print("Data classified as authentic")
            return True
        else:
            print("Data classified as inauthentic")
            return False
    except(KeyError):
        print("Data classified as inauthentic")
        return False
    

def _construct_new_entry():
    return {"class": {}, "vectors": []}


app = Flask(__name__)
CORS(app)
@app.route('/', methods=['POST'])
def result():
    global myary, mymodel, data
    new_data =dict(request.form)
    try:
        if(new_data["retrain"][0]=="True"):
            myary,usrs = get_ary()
            mymodel = TrainedModel(myary)
            labels = mymodel.get_labels()
            tmpcount = 0
            for i in data:
                data[i]["class"]={}
            for i in range(len(usrs)):
                try:
                    data[usrs[i]]["class"][str(labels[i])]+=1
                except(KeyError):
                    data[usrs[i]]["class"][str(labels[i])]=1
            write_json()
    except(KeyError):
        handle_new_vec(new_data, mymodel)
        print(json.dumps(data, indent=2))
    return ('',201)
if __name__ == '__main__':
    data = read_json()
    myary, usrs= get_ary()
    mymodel= TrainedModel(myary)
    app.run(host='10.63.201.94',debug=True,port=6969)

