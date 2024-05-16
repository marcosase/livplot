import pandas as pd
import seaborn as sns
import cufflinks as cf
#import plotly
from plotly.offline import iplot
import time
import sys
import numpy as np
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('template.ui', self) # Load the .ui file
        self.select_btn.clicked.connect(self.open_file)
        self.head_btn.clicked.connect(self.select_header) # Remember to pass the definition/method, not the return value!
        self.plot_btn.clicked.connect(self.plot)#button to plot stuff
        self.show() # Show the GUI
 
    def open_file(self):
        global file_open
        file_open = QFileDialog.getOpenFileName()
        self.label.setText(file_open[0])
        return file_open[0]
    
    def select_header(self):
        global cust, lot_line, cell_line, column_name, hdr_line
        self.x_cmb_box.clear()
        self.y_cmb_box.clear()
        self.file = self.open_file()
        with open(self.file) as f:
            n_col = len(f.readlines()[-1].split(','))
            f.close()

        column_name = []
        with open(self.file) as f:
           
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
            f.close()
        return cust, lot_line, cell_line, column_name 
    
    def plot(self):
        print(cust, lot_line, cell_line, column_name, file_open[0], hdr_line)
        x_axis = self.x_cmb_box.currentText()
        y_axis = self.y_cmb_box.currentText()
        print("***************")
        print(x_axis, y_axis)
        df = pd.read_csv(file_open[0], skiprows = hdr_line+2, names=column_name)
        print(df.head())
        if x_axis == y_axis:
            msg = QMessageBox()
            msg.setWindowTitle("Error!")
            msg.setText("Select different axis to plot!")
            x = msg.exec_()
            sys.exit()
    
        df.iplot(kind='scatter', x=x_axis, y=y_axis)

        

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()