# -*- coding: utf-8 -*-

import csv
import sys
import matplotlib
from PyQt5.QtWidgets import *
from PyQt5 import uic
from AvgGraph import LogInDialog
from FinClawer import FinanceClawer
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QTableWidgetItem
from FinLearning import FinanceDeeplearning
import numpy as np

import matplotlib.font_manager as fm
from PyQt5.QtWidgets import (QApplication, QDialog)

font_path = "data/H2MJRE.TTF"
font_name = fm.FontProperties(fname=font_path).get_name()
matplotlib.rc('font',family=font_name)
matplotlib.rcParams['axes.unicode_minus'] = False
CalUI = "_uiFiles/StockSorter_Main.ui"

class MainDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self, None)
        self.ui = uic.loadUi(CalUI, self)
        self.stockNameAutoComplete()
        self.search_pushButton.clicked.connect(lambda state, button = self.search_pushButton : self.searchClicked(state, button))
        self.reset_pushButton.clicked.connect(lambda state, button = self.reset_pushButton : self.resetCliked(state, button))
        self.sort_pushButton.clicked.connect(lambda state, button = self.sort_pushButton : self.deepLearningClicked(state, button))
        self.graph_pushButton.clicked.connect(self.pushButtonClicked)

    def searchClicked(self, state, button):

        self.answer_label.setText("")

        for i in range(1, 4, 2):
                for j in range(0, 5):
                    self.tableWidget.takeItem(i,j)

        self.CodeText = self.stockCode_textEdit.text()

        if(self.CodeText.isdigit() == False):
            self.inputtedStockName = self.CodeText
            self.stockDictionary = dict(self.koreanStockList)
            self.CodeText = self.stockDictionary.get(self.inputtedStockName)

        try:
            self.clawer = FinanceClawer(self.CodeText)
            self.PassingfinanceData = self.clawer.getFinanceInfo()
            self.PassingStockname = self.clawer.getStockName()
            self.PassingStockExchange = self.clawer.getExchange()
            self.tableWidget.setItem(1,0, QTableWidgetItem(self.clawer.getStockName()))
            self.tableWidget.setItem(1,1, QTableWidgetItem(self.clawer.getCodeNum()))
            self.tableWidget.setItem(1,2, QTableWidgetItem(self.clawer.getStockPrice()+ "원"))
            self.tableWidget.setItem(1,3, QTableWidgetItem(self.clawer.getMarketCap() +"억원"))
            self.tableWidget.setItem(1,4, QTableWidgetItem(self.clawer.getForignRate() + "%"))
            self.tableWidget.setItem(3,0, QTableWidgetItem(self.clawer.getPER() + "배"))
            self.tableWidget.setItem(3,1, QTableWidgetItem(self.clawer.getPBR() + "배"))
            self.tableWidget.setItem(3,2, QTableWidgetItem(self.clawer.getReserveRation() + "%"))
            self.tableWidget.setItem(3,3, QTableWidgetItem(self.clawer.getDebtRatio() + "%"))
            self.tableWidget.setItem(3,4, QTableWidgetItem(self.clawer.getDividendYieldRatio() + "%"))
        except Exception as e:
            print(e)
            QMessageBox.about(self, "Error", "입력하신 주식정보를 불러오지 못하였습니다.\n신규상장 회사의 경우 재무정보가 부족하여 재무제표 업로드에 실패할 수 있습니다..")
            pass

    def resetCliked(self, state, button):
        self.answer_label.setText("")
        self.stockCode_textEdit.setText("")
        self.PassingfinanceData = None
        for i in range(1, 4, 2):
            for j in range(0, 5):
                self.tableWidget.takeItem(i, j)

    def deepLearningClicked(self, state, button):
        try:
            self.deepLearner = FinanceDeeplearning(self.CodeText)
            self.learningAnswer = self.deepLearner.stockSort()
            print(self.learningAnswer)
            self.answer_label.setText(self.learningAnswer)
        except Exception as e:  # 오류 이유 반환
            print(e)

    def stockNameAutoComplete(self):
        self.koreanStockList = []
        koreanStockListCSV = open('data/KoreaStockList.csv', 'r', encoding='UTF8')
        stockListReader = csv.reader(koreanStockListCSV)

        for row in stockListReader:
            self.koreanStockList.append(row)

        koreanStockListCSV.close()
        self.FixedkoreanStockList = np.array(self.koreanStockList).flatten().tolist()
        completer = QCompleter(self.FixedkoreanStockList)
        self.stockCode_textEdit.setCompleter(completer)

    def pushButtonClicked(self):
        self.passData =  self.PassingfinanceData
        self.passStockname = self.PassingStockname
        self.passStockExchange = self.PassingStockExchange
        print(self.passData)
        dlg = LogInDialog(self.passData, self.passStockname,self.passStockExchange)
        dlg.exec_()

app = QApplication(sys.argv)
main_dialog = MainDialog()
main_dialog.show()
app.exec_()