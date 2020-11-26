import numpy as np
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
        self.x=[]   #Значения tau
        self.new_y=[]   #Результат вычисления
        self.a=0
        self.b=0  #Показатель Херста


    def rrange(self, tau, val): # Вычисление размаха для текущего tau
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
        for i in self.x:
            self.res_g.append(self.Fx(i))


if __name__ == '__main__' :
    my_calc=RS_analysis(1, 1, 'F:/Proba.txt')
    my_calc.analysis()
    print(my_calc.b)



