
import pandas as pd
#import seaborn as sns
#import cufflinks as cf
#import plotly
#from plotly.offline import iplot
import time
import sys
import numpy as np
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QVBoxLayout
import pyqtgraph as pg

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        pg.setConfigOption('background', 'w') #before loading widget
        pg.setConfigOption('foreground', 'k')
        super(Ui, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('template.ui', self) # Load the .ui file
        self.select_btn.clicked.connect(self.open_file)
        self.clear_btn.clicked.connect(self.clear_plot)
        self.plot_btn.clicked.connect(self.plot)#button to plot stuff
        self.plot2_btn.clicked.connect(self.plotx2)#button to plot stuff
        self.plotter.plotItem.showGrid(True, True, 0.7)
        self.show() # Show the GUI
 
    def open_file(self):
        global file_open
        file_open = QFileDialog.getOpenFileName()
        self.label.setText(file_open[0].split('/')[-1])
        print('*********')
        self.select_header(file_open[0])
        return 
    
    def select_header(self, file):
        global cust, lot_line, cell_line, column_name, hdr_line
        self.x_cmb_box.clear()
        self.y_cmb_box.clear()
        self.y2_cmb_box.clear()
        
        with open(file) as f:
            n_col = len(f.readlines()[-1].split(','))
            f.close()

        column_name = []
        with open(file) as f:
           
            for i, line in enumerate(f):
                if 'Customer' in line:
                    cust = line.split(' ')[-1].replace('\n','')            
                
                if 'LotID' in line or 'Batch' in line: 
                    lot_line = line.split(' ')[-1].replace('\n','')             
                                
                if 'Cell' in line: 
                    cell_line = line.split(' ')[-1].replace('\n','')

                if ('Current' in line) or ('I_soa' in line) or ('Wavelength' in line):
                    hdr_line = i
                    for j in range(n_col):
                        column_name.append(line.split(',')[2*j].replace('"', ''))
            print(column_name)
            self.x_cmb_box.addItems([k for k in column_name])
            self.y_cmb_box.addItems([k for k in column_name])
            self.y2_cmb_box.addItems([k for k in column_name])
            f.close()
        return cust, lot_line, cell_line, column_name
    
    def plot(self):
        print(cust, lot_line, cell_line, column_name, file_open[0], hdr_line)
        x_axis = self.x_cmb_box.currentText()
        y_axis = self.y_cmb_box.currentText()
        print("***************")
        df = pd.read_csv(file_open[0], skiprows = hdr_line+2, names=column_name)
        print(df.head())
        x_label = str(x_axis)
        y_label = str(y_axis)
        title = 'LIV' #to be change for the actual name
        self.set_graph(title, x_label, y_label)
        self.plotter.plot(df[x_axis], df[y_axis], symbol='o', pen=(np.random.randint(0,255),np.random.randint(0,255),np.random.randint(0,255)), symbolPen='b', symbolBrush=(np.random.randint(0,255),np.random.randint(0,255),np.random.randint(0,255)), symbolSize=8, name='_'.join(file_open[0].split('_')[1:3]))

    def plotx2(self):

        print('Not working yet')
        # p1 = self.plotter.plotItem

        # ###Plotting the first axes
        # self.plotter.clear()
        # x_axis = self.x_cmb_box.currentText()
        # y_axis = self.y_cmb_box.currentText()
        # y2_axis = self.y2_cmb_box.currentText()
        # print("***************")
        # df = pd.read_csv(file_open[0], skiprows = hdr_line+2, names=column_name)
        # print(df.head())
        # x_label = str(x_axis)
        # y_label = str(y_axis)
        # title = 'LIV' #to be change for the actual name
        # self.set_graph(title, x_label, y_label)
        # #self.plotter.plot(df[x_axis], df[y_axis], symbol='o', pen=(np.random.randint(0,255),np.random.randint(0,255),np.random.randint(0,255)), symbolPen='b', symbolBrush=(np.random.randint(0,255),np.random.randint(0,255),np.random.randint(0,255)), symbolSize=8, name='_'.join(file_open[0].split('_')[1:3]))
        # p1.plot(df[x_axis], df[y_axis], symbol='o', pen=(np.random.randint(0,255),np.random.randint(0,255),np.random.randint(0,255)), symbolPen='b', symbolBrush=(np.random.randint(0,255),np.random.randint(0,255),np.random.randint(0,255)), symbolSize=8, name='_'.join(file_open[0].split('_')[1:3]))
        # ###

        # p2 = pg.ViewBox()
        # p1.showAxis('right')
        # p1.scene().addItem(p2)
        # p1.getAxis('right').linkToView(p2)
        # p2.setXLink(p1)
        # p1.getAxis('right').setLabel('axis2', color='#0000ff')

        # p2.setGeometry(p1.vb.sceneBoundingRect())
        # # #adding  an item without rescaling
        # p2.addItem(pg.PlotCurveItem(df[x_axis].values, df[y2_axis].values, symbol='o', pen=(np.random.randint(0,255),np.random.randint(0,255),np.random.randint(0,255)), symbolPen='b' ))
        
       


    def clear_plot(self):
        self.plotter.clear()

    def set_graph(self,titulo,eixo_x,eixo_y):
            p1 = self.plotter
            # THESE PARAMETERS ARE FOR RESIZING AND MOVING THE POSITION OF THE LEGEND BOX
            # I INCREASED X-SIZE AND Y-OFFSET
            p1.addLegend(size=(110, 0) ,offset=(10, 10))
            p1.setTitle('<font size="2">Active Power</font>') #,**titleStyle)
            a = p1.getAxis('top')
            a.showValues='false'
            a = p1.getAxis('bottom')
            p1.showAxis('left')
            a = p1.getAxis('left')
            p1.showAxis('right')
            a = p1.getAxis('right')
            p1.showLabel('left', show=True)
            p1.showLabel('right', show=True)
            p1.showGrid(x=True, y=True, alpha=0.1)
            titleStyle = {'color': '#000', 'size': '18pt'}
            p1.setTitle(titulo, **titleStyle)
            # SET AND CHANGE THE FONT SIZE AND COLOR OF THE PLOT AXIS LABEL
            labelStyle = {'color': '#000', 'font-size': '16px'}
            p1.setLabel('bottom', eixo_x, **labelStyle)
            p1.setLabel('left', eixo_y, **labelStyle)
            p1.setLabel('top',)

        

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()