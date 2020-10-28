import numpy as np
import math
import matplotlib.pyplot as plt

# Метод наименьших квадратов

def LS(x, y):
    sX=0
    sY=0
    sXY=0
    sXX=0
    n=len(x)
    for i in x: sX=math.log(i)
    for i in x: sXX=np.power(math.log(i), 2)
    for i in y: 
        if (i>0): sY=math.log(i)
    for i in range(len(x)): 
        if (y[i]>0): sXY=math.log(x[i])*math.log(y[i])
    b=(n*sXY-sX*sY)/(n*sXX-np.power(sX, 2))
    a=math.exp((sY-b*sX)/n)
    return [a, b]

def LSsq(x, y):
    sX=sum(x)
    sY=sum(y)
    sXY=sum(x[i]*y[i] for i in range(len(x)))
    sXX=sum(np.power(x, 2))
    sYY=sum(np.power(y, 2))
    n=len(x)
    a=(sX*sY-n*sXY)/(np.power(sX, 2)-n*sXX)
    b=(sX*sXY-sXX*sY)/(np.power(sX, 2)-n*sXX)
    return [a, b]
    

f=open(r"C:\Users\student_02\Desktop\test.dat")
fromfile=f.readlines()
tau=2
delta_tau=2
T=len(x)
y=[float(i) for i in fromfile]
x=[i+1 for i in range(len(y))]

print(LSsq(x, y))
