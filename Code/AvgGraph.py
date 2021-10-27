from PyQt5.QtWidgets import QDialog, QHBoxLayout
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np

class LogInDialog(QDialog):
    def __init__(self, inputtedFinanceList, inputtedStockname,inputtedStockExchange):
        super().__init__()
        self.originalfinanceData = inputtedFinanceList
        self.financeData = inputtedFinanceList
        self.stockName = inputtedStockname
        self.stockExchange = inputtedStockExchange
        self.N = 6
        self.value2 = [1.72, 45.06, 1.71, 0.68, 62.89, 10.1]
        self.value3 = [17.05, 12.32, 0.86, 2.22, 67.33, 35.7]
        self.originalData = self.financeData[0][0]
        self.financeData[0][0] = self.financeData[0][0] / 1000
        self.value = sum(self.financeData, [])
        self.financeData[0][0] = self.originalData
        self.setupUI()

    def setupUI(self):
        self.x = np.arange(self.N)
        self.width = 0.35
        fig, ax = plt.subplots()
        rects1 = ax.bar(self.x - self.width/2 , self.value, self.width, label=self.stockName)

        if(self.stockExchange.find("코스닥")) != -1 :
            rects2 = ax.bar(self.x + self.width/2 , self.value2, self.width, label='코스닥 평균치')
        else:
            rects2 = ax.bar(self.x + self.width / 2, self.value3, self.width, label='코스피 평균치')
        ax.set_xticks(self.x + self.width / 2)
        ax.legend()
        ax.set_xticklabels(['시가총액', 'PER', 'PBR', '시가배당률', '부채비율', '외인비율'])

        canvas = FigureCanvas(fig)
        canvas.draw()
        lay = QHBoxLayout()
        self.setLayout(lay)
        lay.addWidget(canvas)
        canvas.show()