import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd

class FinanceClawer:
    def __init__(self, stockCode):
        self.URL = "https://finance.naver.com/item/main.nhn?code=" + stockCode
        self.stockURL = requests.get(self.URL)
        self.html = self.stockURL.text
        self.soup = BeautifulSoup(self.html, 'html.parser')
        self.slicing()

    def slicing(self):
        self.finance_html = self.soup.select('div.section.cop_analysis div.sub_section')[0]
        self.th_data = [item.get_text().strip() for item in self.finance_html.select('thead th')]
        self.annual_date = self.th_data[3:7]
        self.quarter_date = self.th_data[7:13]
        self.finance_index = [item.get_text().strip() for item in self.finance_html.select('th.h_th2')][3:]
        self.finance_data = [item.get_text().strip() for item in self.finance_html.select('td')]
        self.finance_data = np.array(self.finance_data)
        self.finance_data.resize(len(self.finance_index), 10)
        self.finance_date = self.annual_date + self.quarter_date
        self.finance = pd.DataFrame(data=self.finance_data[0:, 0:], index=self.finance_index, columns=self.finance_date)

    def getAnnualFin(self):
        self.annual_finance = self.finance.iloc[:, :4]
        return self.annual_finance

    def getQuarterFin(self):
        self.quarter_finance = self.finance.iloc[:, 4:]
        return self.quarter_finance[2]

    def getStockName(self):
        self.title = self.soup.select('div.h_company h2 a')[0].text
        return self.title

    def getForignRate(self):
        self.forignRate = self.soup.select('div.gray em')[2].text.replace('%', '')
        return self.forignRate

    def getStockPrice(self):
        self.stockPrice = self.soup.select('p.no_today span.blind')[0].text
        return self.stockPrice

    def getMarketCap(self):
        self.marketCap = self.soup.find("em", id="_market_sum").text.replace(',', '').replace('\t' , "").replace('\n', "")
        if self.marketCap.find("조") != -1: #
            self.zoIndex = self.marketCap.find("조")
            self.zoNum = self.marketCap[0:self.zoIndex]
            self.leftNum = self.marketCap[self.zoIndex+1:]
            self.fixedMarketCap = str(int(self.leftNum) + (int(self.zoNum) * 10000))
            return self.fixedMarketCap
        return self.marketCap

    def getCodeNum(self):
        self.stockPrice = self.soup.select('div.description span.code')[0].text
        return self.stockPrice

    def getPER(self):
        if self.soup.find("em", id="krx_per") == None and self.finance_data[10][2] == '':
        #    print("예상 PER이 없고, 작년 기준 PER이 없어 추정치로 대체되었습니다.")
            self.lastYearPER = self.finance_data[10][3]
            return self.lastYearPER
        elif self.soup.find("em", id="krx_per") == None and self.finance_data[10][2] != '':
            self.lastYearPER = self.finance_data[10][2]
        #    print("예상 PER이 없어, 작년 기준 PER로 대체되었습니다.")
            return self.lastYearPER
        else:
            self.lastYearPER = self.soup.find("em", id="krx_per").text.strip()
        return self.lastYearPER

    def getPBR(self):
        self.pbr = self.soup.find("em", id="_pbr").text.strip()
        return  self.pbr

    def getReserveRation(self):
        self.reserveRation =self.finance_data[8][8]
        return self.reserveRation

    def  getDebtRatio(self):
        self.debtRatio = self.finance_data[6][8].replace(',', '')
        return self.debtRatio

    def getDividendYieldRatio(self):
        try:
            self.judgment = float(self.finance_data[14][2])
        except Exception as e:
            print(e)
            return '0'
        self.dividendYieldRatio = self.finance_data[14][2]
        return self.dividendYieldRatio

    def getExchange(self):
        self.exchange = self.soup.select('div.first tr td')[1].text
        return self.exchange

    def getFinanceInfo(self):
        returnedList = []
        rawList =[self.getMarketCap(), self.getPER(), self.getPBR(), self.getDividendYieldRatio(), self.getDebtRatio(), self.getForignRate()]
        rawList = list(map(float, rawList))
        returnedList.append(rawList)
        return returnedList

if __name__=='__main__':
    clawer = FinanceClawer("095660")
    s = clawer.getExchange()
    print(s)

