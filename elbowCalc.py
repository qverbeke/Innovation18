# -*- coding: utf-8 -*-
"""
Created on Wed Jul 25 10:00:21 2018

@author: PillaiAr
"""

myArray = [[1,3.4577],[2,1.7687],[3,0.88199],[4,0.7587],[5,0.6635],[6,0.6066],[7,0.50937],[8,0.43613],[9,0.33333]]

def ratioCalc(a,b,c,i):
    top = b[1]-a[1]
    bottom = c[1]-b[1]
    ratio = top/bottom
    return ratio

max = 0


n = len(myArray)


if(myArray[0][1] < myArray[-1][1]):
    i = 1
    while(i < n):
        ratio = ratioCalc(myArray[i-1],myArray[i],myArray[i+1],i)
        if(ratio >= max):
            max = ratio
        #else:
         #   break
        i+=1

else:
    for i in range(len(myArray)-2,0,-1):
        ratio = ratioCalc(myArray[i+1],myArray[i],myArray[i-1],i)
        if(ratio >= max):
            max = ratio
        #else:
        #    break

    
elbow = myArray[i+1]
print(elbow)
