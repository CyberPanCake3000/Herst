import numpy as np
import math
import matplotlib.pyplot as plt

def Average(tau, val):
    sum=0
    for i in val:
        sum += i
    res = sum/tau
    return res


def SumAverage_Scope(tau, val):
    sum=0
    ave = Average(tau, val)
    min=val[1]-ave
    max=val[1]-ave
    for i in val:
        sum += i - ave
        if sum<min: min = sum
        if sum>max: max = sum
    CKO(tau, sum)
    return max-min


def CKO(tau, sumaverage):
    return np.power(np.power(sumaverage, 2)/(tau - 1), 0.5)

# Метод наименьших квадратов
def LS(x, y):
    t=len(x)
    medX=0
    medY=0
    medXX=0
    medXY=0
    for i in x: medX+=math.log(i)
    for i in y: medY+=math.log(i)
    for i in x: medXX+=np.power(math.log(i), 2)
    for i in range(len(x)): medXY+=math.log(x[i])*math.log(y[i])
    b=(t*medXY-medX*medY)/(t*medXX-np.power(medX, 2))
    a=math.exp((medY-b*medX)/t)
    return a


def PowFx(a, b, x):
    return a*np.power(x, b)

x=[2.5, 3,3.3,4,4.4,5,5.5,6,6.5,7,7.5,8,8.5]
y=[4.4,3.6,3,2.7,2.1,1.8,1.9,1.5,1.4,1.3,1.2,1.1,1.1]
a=LS(x, y)[0]
b=LS(x, y)[1]
plt.scatter(x, y, c="red")
for i in range(20):
    plt.plot(i, LinearFx(a, b, i))
    # test value LS([0.1, 0.2, -0.1, 0.5, 0.002], [0, 1, 2, 3, 4 ])
# test value from site mathhelp planet x=[2.5, 3,3.3,4,4.4,5,5.5,6,6.5,7,7.5,8,8.5] y=[4.4,3.6,3,2.7,2.1,1.8,1.9,1.5,1.4,1.3,1.2,1.1,1.1]
