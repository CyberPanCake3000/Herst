import numpy as np
import math
<<<<<<< HEAD
from PyQt5.QtWidgets import QAction, QApplication, QFileDialog, QMessageBox
from PyQt5 import QtWidgets, QtGui, QtCore
import Herst_gui
import matplotlib
matplotlib.use('QT5Agg')
import sys
import pyqtgraph as pg
from openpyxl import load_workbook
import openpyxl


class RS_analysis:

    def __init__(self, data_y, tau=1, del_tau=1):
        self.tau = tau #начальная точка
        self.del_tau = del_tau #шаг
        self.data_y = data_y
        self.res_g = []   #Результат построения степенной регрессии
        self.x = []   #Значения tau
        self.new_y = []   #Результат вычисления
        self.a = 0
        self.b = 0  #Показатель Херста
        self.analysis()

    # @property
    # def a(self):
    #     return self.__a
    #
    # @property
    # def b(self):
    #     return self.__b
    #
    # def set_tau(self, tau):
    #     self.__tau = tau
    #
    # def set_del_tau(self, del_tau):
    #     self.__del_tau = del_tau
    #
    # def set_data_y(self, data_y):
    #     self.__data_y = data_y


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
        sX=0
        sY = 0
        sXY = 0
        sXX = 0
        n = len(y)
        for i in x:
            sX += math.log(i)
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
        self.new_y = []
        for i in np.arange(1, len(self.data_y), self.del_tau):
            def_R = self.rrange(i, self.data_y[:i])
            def_S = self.SCO(i, self.data_y[:i])
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

    def doTuple(self):
        result_tuple = []
        result_tuple.append(['a=', self.a])
        result_tuple.append(['b=', self.b])
        result_tuple.append(['x', 'R/S', 'Степенная регрессия'])
        for i in range(len(self.new_y)):
            result_tuple.append([self.x[i], self.new_y[i], self.res_g[i]])
        return result_tuple

class Herst_window(QtWidgets.QMainWindow, Herst_gui.Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Показатель Херста')
        self.datafile = []
        self.result_tuple = []
        # self.pushButton.clicked.connect()
        self.lineEdit.setText('1')
        self.lineEdit_2.setText('1')
        self.pushButton.setEnabled(0)

        openFile = QAction('Открыть файл', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Открыть файл')
        openFile.triggered.connect(self.showDialog)
        self.menu.addAction(openFile)

        self.GraphWidget.setBackground('w')
        style = {'color': 'b', 'font-size': '20px'}
        self.GraphWidget.setLabel('left', 'R/S', **style)
        self.GraphWidget.setLabel('bottom', 'time', **style)
        self.GraphWidget.addLegend()

        saveData = self.menu_2.addAction("Сохранить данные в Excel")
        saveData.triggered.connect(self.saveData)

        # saveFile_Plot = QAction('Сохранить график и данные', self)


        # exit = QAction('Выйти', self)

        # self.menu_3.action_5.trigger.connect(self.savePlot)
        # self.grid.valueChanged.connect(self.showGrid)

    def set_herst_num(self, value='-'):
        self.herst_num.setText(value)

    def set_frac(self, value='-'):
        self.frac.setText(value)

    def set_mandelb(self, value='-'):
        self.mandelb.setText(value)

    def set_corr(self, value='-'):
        self.corr.setText(value)

    def set_plot(self, x, y, pen, lbl='-'):
        self.GraphWidget.plot(x, y, pen=pen, name=lbl)

    def set_resultTuple(self, tup):
        self.result_tuple = tup

    def get_tau(self):
        return int(self.lineEdit.text())

    def get_delta_tau(self):
        return int(self.lineEdit_2.text())

    def showDialog(self):
        fname = QFileDialog.getOpenFileName(self, "Открыть текстовый файл", "/home", "Excel (*.xlsx);;Data (*.dat);; Text (*.txt)")[0]
        if (fname.find('.dat')!=-1 or fname.find('.txt')!=-1):
            fromfile = open(fname, 'r')
            lines = fromfile.readlines()
            self.datafile = [float(i) for i in lines]
            fromfile.close()
        else:
            fromfile = load_workbook(fname)['RC']
            sheet_range = fromfile['A']
            for cell in sheet_range:
                self.datafile.append(float(cell.value))

        if len(self.datafile) != 0:
            self.pushButton.setEnabled(1)

    def saveData(self):
        fname = QFileDialog.getSaveFileName(self, "Сохранить файл данных", "/home", "Excel (*.xlsx)")[0]
        wb = openpyxl.Workbook()
        wb.create_sheet(title='Результат', index=0)
        sheet = wb['Результат']
        for i in range(len(self.result_tuple)):
            sheet.append(self.result_tuple[i])
        wb.save(fname)

def visualization(self):

    tau = int(window.lineEdit.text())
    del_tau = int(window.lineEdit_2.text())
    RS = RS_analysis(window.datafile, tau, del_tau)
    window.set_resultTuple(RS.doTuple())
    window.set_herst_num(str(round(RS.b, 4)))
    window.set_mandelb(str(round(1/RS.b, 4)))
    window.set_frac(str(round(2-RS.b, 4)))
    window.set_corr(str(round(2**(2*RS.b-1)-1, 4)))
    pen = pg.mkPen(color=(1, 88, 239), width=5)
    window.set_plot(RS.x, RS.new_y, pen, 'Обработанные данные')
    pen = pg.mkPen(color=(255, 191, 0), width=5)
    window.set_plot(RS.x, RS.res_g, pen, 'Регрессия y=a*x^b')

app = QApplication(sys.argv)
window = Herst_window()
window.pushButton.clicked.connect(visualization)

window.show()
app.exec_()

=======
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
a=LS(x, y)[0]
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
>>>>>>> origin/master
