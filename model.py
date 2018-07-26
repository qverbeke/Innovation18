from sklearn.cluster import KMeans
import numpy as np
import elbowCalc as ebc
from scipy.spatial.distance import cdist
import json


class TrainedModel:
    def __init__(self, myary):
        distortions = []
        for k in range(1,20):
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
def write_json(data):
    with open("datastore.json", "w") as f:
        json.dump(data, f)
def get_ary(data):
    count = 0
    arylen = 0
    for i in data:
        count+=len(data[i]["vectors"])
        if arylen==0:
            arylen=len(data[i]["vectors"][0])
    result = np.empty(shape=(count, arylen))
    ind = 0
    for i in data:
        for j in data[i]["vectors"]:
            result[ind] = j
            ind+=1
    return result
mydata = read_json()
myary = get_ary(mydata)

thing = TrainedModel(myary)
