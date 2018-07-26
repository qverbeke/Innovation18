# -*- coding: utf-8 -*-
"""
Created on Wed Jul 25 10:00:21 2018

@author: PillaiAr
"""
def get_k(myArray):
    def ratioCalc(a,b,c,i):
        top = c[1]-b[1]
        bottom = b[1]-a[1]
        ratio = top/bottom
        
        return ratio

    n = len(myArray)
    max = 0
    
    if(myArray[0][1] < myArray[-1][1]):
        i = 1
        #max = 0
        while(i < n):
            ratio = ratioCalc(myArray[i-1],myArray[i],myArray[i+1],i)
            if(ratio >= max):
                max = ratio
                place = i
            #else:
             #   break
            i+=1

    else:
        #min = 1000000
        for i in range(len(myArray)-2,0,-1):
            ratio = ratioCalc(myArray[i+1],myArray[i],myArray[i-1],i)
            if(ratio >= max):
                max = ratio
                place = i
            #else:
            #    break

        
    elbow = myArray[place]
    return elbow
