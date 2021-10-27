from keras.models import load_model
import pandas as pd
from sklearn.preprocessing import StandardScaler
import numpy as np
from FinClawer import FinanceClawer

class FinanceDeeplearning:
    def __init__(self,codeNum):
        self.codeNum = codeNum
        print("딥러닝 객체생성시도 중 코드넘버 " + self.codeNum)
        self.model = load_model("DeeplearningModel/my_stockmodel.h5")
        self.scaler = StandardScaler()

    def adJustPer(self, num): #적자회사일 경우, 딥러닝에 혼란을 주어, 지수함수를 활용하여 마이너스값을 전처리하여 사용하였다.
        if num>0:
            return num
        return 900*np.exp(num/10) + 100

    def stockSort(self):
        self.clawer = FinanceClawer(self.codeNum)
        self.adjustedPER = self.clawer.getPER()
        self.originalList = self.clawer.getFinanceInfo()
        if(float(self.adjustedPER)  < 0):
            self.originalList[0][1] = self.adJustPer(float(self.adjustedPER))
        self.finDataframe = pd.DataFrame(self.originalList, columns=['MarketCap','PER', 'PBR', 'DividendYield' , 'DebtRatio' ,'ForignRatio'])

        df = pd.read_csv("DeeplearningModel/Stock.csv", names=["StockCode", "StockName", "Prcie",
                                                                  "MarketCap", "PER", "PBR", "DividendYield",
                                                                  "DebtRatio", "ForignRatio", "Retentionrate", "class"])

        df = df[['MarketCap', 'PER', 'PBR', 'DividendYield', 'DebtRatio', 'ForignRatio']]
        df = pd.concat([self.finDataframe ,df]).reset_index(drop = True)
        self.rawData = self.scaler.fit_transform(df)
        self.rawData = self.rawData[0:1]
        self.predictedAnswer = self.model.predict(self.rawData).tolist()
        self.maxPredictedAnswer = max(self.predictedAnswer[0])

        if self.predictedAnswer[0][0] == self.maxPredictedAnswer:
            return "성장주입니다"
        elif self.predictedAnswer[0][1] == self.maxPredictedAnswer:
            return "가치주입니다"
        elif self.predictedAnswer[0][2] == self.maxPredictedAnswer:
            return "배당주입니다"
        else:
            return "투자유의주입니다"

if __name__=='__main__':
    clawer = FinanceDeeplearning("044380")
    print(clawer.stockSort())

