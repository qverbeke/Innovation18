from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt


"""
mydata = [[1, 2], [1, 4], [1, 0],[4, 2.5], [4, 4], [4, 0]]
pltdatax = [1,1,1,4,4,4]
pltdatay = [2,4,0,2.5,4,0]

"""
myary = np.random.randn(100,2)

kmeans = KMeans(n_clusters=4, random_state=0).fit(myary)

pltary = [[[],[]],[[],[]],[[],[]],[[],[]]]
for i in range(len(myary)):
    pltary[kmeans.labels_[i]][0].append(myary[i][0])
    pltary[kmeans.labels_[i]][1].append(myary[i][1])
    
plt.scatter(pltary[0][0],pltary[0][1], color="r")
plt.scatter(pltary[1][0],pltary[1][1],color="b")
plt.scatter(pltary[2][0],pltary[2][1],color="g")
plt.scatter(pltary[3][0],pltary[3][1],color="c")
plt.show()

print(kmeans.labels_)
print(myary)
