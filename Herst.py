import numpy as np
import math
import matplotlib.pyplot as plt

def Average(tau, val):
    sum=0
    for i in val:
        sum += i
    res = sum/tau
    return res


def Range(tau, val):
    sum=0
    ave = Average(tau, val)
    min=val[1]-ave
    max=val[1]-ave
    for i in val:
        sum += i - ave
        if sum<min: min = sum
        if sum>max: max = sum
    return max-min


def SCO(tau, sumaverage):
    return np.power(np.power(sumaverage, 2)/(tau - 1), 0.5)

# Метод наименьших квадратов
def LS(x, y):
    t=len(x)
    medXY=0
    medX=sum([math.log(c) for c in x])
    medY=sum([math.log(c) for c in y])
    medXX=sum([np.power(math.log(c), 2) for c in x])
    for i in range(len(x)): medXY+=math.log(x[i])*math.log(y[i])
    b=(t*medXY-medX*medY)/(t*medXX-np.power(medX, 2))
    a=math.exp((medY-b*medX)/t)
    return [a, b]


def LinearFx(x):
    return a+b*x 


y=[4.4,3.6,3,2.7,2.1,1.8,1.9,1.5,1.4,1.3,1.2,1.1,1.1]
tau0=2
delta_tau=2
x=[i+1 for i in range(len(y))]
a=LS(x, y)[0]
b=LS(x, y)[1]

ln=[LinearFx(c) for c in x]

plt.figure(figsize=(5, 5))
plt.subplot(2,1,1)
plt.scatter(x, y, c="red")
plt.plot(x, ln)
plt.subplot(2,1,2)
nowtau=tau
while nowtau<len(y):
    defR=Range(nowtau, y)
    defS=SCO(nowtau, y)
    plt.plot(math.log(x), math.log(defR/defS))
    # test value LS([0.1, 0.2, -0.1, 0.5, 0.002], [0, 1, 2, 3, 4 ])
# test value from site mathhelp planet x=[2.5, 3,3.3,4,4.4,5,5.5,6,6.5,7,7.5,8,8.5] y=[4.4,3.6,3,2.7,2.1,1.8,1.9,1.5,1.4,1.3,1.2,1.1,1.1]
