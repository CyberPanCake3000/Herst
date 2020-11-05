import numpy as np
import math
import matplotlib.pyplot as plt
from tkinter import *

# np.seterr(divide='ignore', invalid='ignore')


def average(tau, val):
    # Вычисление среднего значения для текущего tau
    s = sum(val)
    return (s/tau)


def rrange(tau, val):
    # Вычисление размаха для текущего tau
    sum=0
    ave = average(tau, val)
    min=val[1]-ave
    max=val[1]-ave
    for i in val:
        sum += i - ave
        if sum<min: min = sum
        if sum>max: max = sum
    return (max-min)


def SCO(tau, val):
    res = 0
    medium = average(tau, val)
    s = 0
    for i in val:
        s+=np.power(i-medium, 2)
    res=np.power(s / (tau - 0.99999999), 0.5)
    return res
    # return np.power(np.power(sumaverage, 2)/(tau - 1), 0.5)


def LinearFx(x):
    return a+b*x


# Метод наименьших квадратов

def LS(x, y):
    # sX = sum([math.log(i) for i in x])
    sX=1
    sY = 1
    sXY = 1
    sXX = 1
    n = len(x)
    for i in x:
        if(i>0): sX = math.log(i)

    for i in x:
        if (i > 0): sXX = np.power(math.log(i), 2)

    for i in y:
        if (i > 0):
            sY = math.log(i)

    for i in range(len(x)):
        if (x[i]>0 and y[i] > 0): sXY = math.log(x[i]) * math.log(y[i])

    b = (n * sXY - sX * sY) / (n * sXX - np.power(sX, 2))
    a = math.exp((sY - b * sX) / n)
    return [a, b]


f = open(r"C:\Users\student_02\Desktop\test.dat")
fromfile = f.readlines()
tau = 1
delta_tau = 1

y = [float(i) for i in fromfile]
new_y=[]
# x=[i+1 for i in range(len(y))]
x=[]

for i in np.arange(0, len(y), delta_tau):
    def_R=rrange(i+1, y)
    def_S=SCO(i+1, y)
    new_y.append(math.log(def_R / def_S))
    x.append(math.log(i+1))

# print(new_y)
print(LS(x, new_y)[1])
print(2-LS(x, new_y)[1]) #фрактальная размерность
print(1/LS(x, new_y)[1]) #размерность Мандельброта
print(np.power(2, 2*LS(x, new_y)[1]-1)-1) #корреляционное соотношение
root = Tk()
root.title("Показатель Херста")
root.geometry("400x300+300+250")

root.mainloop()


