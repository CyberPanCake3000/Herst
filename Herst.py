import numpy as np
import math
import matplotlib.pyplot as plt
import time
# np.seterr(divide='ignore', invalid='ignore')


def average(tau, val):
    # Вычисление среднего значения для текущего tau
    return (sum(val)/tau)


def rrange(tau, val):
    # Вычисление размаха для текущего tau
    sum=0
    ave = average(tau, val)
    min=val[0]-ave
    max=val[0]-ave
    for i in val:
        sum += i - ave
        if sum<min: min = sum
        if sum>max: max = sum
    return (max-min)


def SCO(tau, val):
    res = 0
    medium = sum(val)/tau
    s = 0
    for i in val:
        # s+=np.power(i-medium, 2)
        s+=(i - medium)**2

    res=(s / (tau - 0.99999999))**0.5
    return res
    # return np.power(np.power(sumaverage, 2)/(tau - 1), 0.5)


def Fx(x):
    return a*(b**x)


# Метод наименьших квадратов

def LS(x, y):
    # sX = sum([math.log(i) for i in x])
    sX=1
    sY = 1
    sXY = 1
    sXX = 1
    n = len(y)
    for i in x:
        sX += math.log(i)
        # sXX += np.power(math.log(i), 2)
        sXX += math.log(i)**2
    for i in y:
        if (i > 0):
            sY += math.log(i)

    for i in range(len(y)):
        if (y[i] > 0):
            sXY += math.log(x[i]) * math.log(y[i])

    b = (n * sXY - sX * sY) / (n * sXX - sX**2)
    # np.power(sX, 2)
    a = math.exp((sY - b * sX) / n)
    return [a, b]


f = open(r"E:\test2.txt")
fromfile = f.readlines()
f.close()
tau = 1
delta_tau = 1

y = np.array([float(i) for i in fromfile])

# plt.plot(y)
new_y=[]
x=[]
# x=[i+1 for i in range(len(y))]
# x=np.array([i+1 for i in range(len(y))])
# t=time.time()
# for i in range(1, len(y), delta_tau):
for i in np.arange(1, len(y), delta_tau):
    def_R=rrange(i, y[:i])
    def_S=SCO(i, y[:i])
    if math.isnan(def_R / def_S): new_y.append(0)
    else: new_y.append(def_R / def_S)
    x.append(i)
# print('lol', time.time()-t)

new_new_y=np.array(new_y)
print(new_new_y[0], x[0])
# new_x=np.array(x)
a=LS(x, new_new_y)[0]
b=LS(x, new_new_y)[1]
print(round(b, 4))
print(round(2-b, 4)) #фрактальная размерность
print(round((1/b), 4))#размерность Мандельброта
print(np.power(2, 2*b-1)-1) #корреляционное соотношение
res_g=[]
for i in x:
    res_g.append(Fx(i))

plt.plot(res_g)
plt.show()



