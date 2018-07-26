from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt
import elbowCalc as ebc
from scipy.spatial.distance import cdist



"""
mydata = [[1, 2], [1, 4], [1, 0],[4, 2.5], [4, 4], [4, 0]]
pltdatax = [1,1,1,4,4,4]
pltdatay = [2,4,0,2.5,4,0]

"""

class TrainedModel:
    def __init__(self, myary):
        self._distortions = []
        for k in range(1,20):
            self._kmeans = KMeans(n_clusters=k, random_state=0).fit(myary)
            self._kmeans.fit(myary)
            self._distortions.append([k,sum(np.min(cdist(myary, self._kmeans.cluster_centers_, 'euclidean'), axis=1))/myary.shape[0]])
        print(ebc.get_k(self._distortions))
        
    def classify_point(self, vec):
        return self._kmeans.predict(vec)
    def retrain(self, myary):
        self._kmeans = KMeans(n_clusters=2, random_state=0).fit(myary)
    def get_labels(self):
        return self._kmeans.labels_
    


myary1 = np.random.randn(100,4)
for i in range(100):
    myary1[i][3]+=100
myary2 = np.random.randn(100,4)
for i in range(100):
    myary2[i][3]-=100
myary3 = np.random.randn(100,4)
myary4 = np.random.randn(100,4)
for i in range(100):
    myary4[i][2]+=100
myary5 = np.random.randn(100,4)
for i in range(100):
    myary5[i][2]-=100
myary=np.concatenate((myary1, myary2,myary3,myary4,myary5), axis=0)

thing = TrainedModel(myary)
#print(thing.classify_point([[0,0,0,-2]]))
#print(thing.get_labels())


#pltary = [[[],[]],[[],[]]]#,[[],[]],[[],[]]]
pltary=[[],[]]
for i in range(len(thing._distortions)):
    pltary[0].append(thing._distortions[i][0])
    pltary[1].append(thing._distortions[i][1])
    
plt.scatter(pltary[0],pltary[1], color="r")
#plt.scatter(pltary[1][0],pltary[1][1],color="b")
#plt.scatter(pltary[2][0],pltary[2][1],color="g")
#plt.scatter(pltary[3][0],pltary[3][1],color="c")
plt.show()
#print(kmeans.labels_)
