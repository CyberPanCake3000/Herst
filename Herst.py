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


f=open(r"C:\Users\student_02\Desktop\test.dat")
fromfile=f.readlines()
y=[float(i) for i in fromfile]
tau=2
delta_tau=2
x=[i+1 for i in range(len(y))]
a=LS(x, y)[0]import numpy as np
import math
import matplotlib.pyplot as plt
import time
# from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication
# from PyQt5.QtGui import QIcon
# from graph_file import *
# np.seterr(divide='ignore', invalid='ignore')


class RS_analysis:

    def __init__(self, tau, del_tau, filename):
        self.tau = tau #начальная точка
        self.del_tau = del_tau #шаг
        self.filename = filename
        self.res_g=[]   #Результат построения степенной регрессии
        self.x=[]   #значения tau
        self.new_y=[]   #Результат вычисления
        self.a=0
        self.b=0  #Показатель Херста

        # analysis()


    def rrange(self, tau, val):
        # Вычисление размаха для текущего tau
        s = 0
        ave = sum(val)/tau
        min = val[0]-ave
        max = val[0]-ave
        for i in val:
            s += i - ave
            if s < min: min = s
            if s > max: max = s
        return max-min


    def SCO(self, tau, val):
        medium = sum(val)/tau
        s = 0
        for i in val:
            s += (i - medium)**2
        return (s / (tau - 0.99999999))**0.5
        # return np.power(np.power(sumaverage, 2)/(tau - 1), 0.5)


    def Fx(self, x):
        return self.a*(x**self.b)


    # Метод наименьших квадратов

    def LS(self, x, y):
        # sX = sum([math.log(i) for i in x])
        sX=0
        sY = 0
        sXY = 0
        sXX = 0
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
        a = math.exp((sY - b * sX) / n)
        return [a, b]


    def analysis(self):
        f = open(self.filename, 'r')
        fromfile = f.readlines()
        f.close()
        y = np.array([float(i) for i in fromfile])
        # new_y = []
        # x = []
        for i in np.arange(1, len(y), self.del_tau):
            def_R = self.rrange(i, y[:i])
            def_S = self.SCO(i, y[:i])
            if math.isnan(def_R / def_S):
                self.new_y.append(0)
            else:
                self.new_y.append(def_R / def_S)
            self.x.append(i)
        self.new_y = np.array(self.new_y)
        self.a = self.LS(self.x, self.new_y)[0]
        self.b = self.LS(self.x, self.new_y)[1]
        # res_g = []
        for i in self.x:
            self.res_g.append(self.Fx(i))


if __name__ == '__main__' :
    my_calc=RS_analysis(1, 1, 'F:/Proba.txt')
    my_calc.analysis()
    print(my_calc.b)
    



b=LS(x, y)[1]

# plt.figure(figsize=(5, 5))
# plt.subplot(2,1,1)
# plt.scatter(x, y, c="red")
# plt.plot(x, ln)
# plt.subplot(2,1,2)
nowtau=tau


PointList=[]
pList=[]
newl=[]

while nowtau<len(y):
    defR=Range(nowtau, y)
    defS=SCO(nowtau, Average(nowtau, y))
    PointList.append(math.log(nowtau))
    pList.append(math.log(defR / defS))
    newl.append(LinearFx(math.log(nowtau)))
    nowtau+=delta_tau

plt.plot(pList, PointList)
plt.plot(newl)
