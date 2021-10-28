## 주식 다중분류기 - 1인 Toy 프로젝트
파이썬 언어와 Keras 라이브러리를  이용해서 주식 개별종목을 Multi Classify하는 학습목적의 Toy 프로젝트입니다.

1. 성장주
2. 가치주
3. 배당주
4. 투자유의주

영웅문 HTS에서 제공된 주식분류 내용을 참고하여 위 분류로 인공지능 다중분류 학습을 위한 Training Set, Validation Set을 구성하였습니다.  

크롤링을 통해 긁어온 금융정보를 바탕으로 학습된 인공지능 모델이 위 4개의 분류 중 어떤 분류의 주식에 제일 가까운 지, 다중분류를 실행합니다.
## 1. 개발환경
<blockquote> 
<p> 언어</p>
</blockquote>
<ul>
<li>Python 3.6</li>
</ul>
<blockquote> 
<p> 프레임워크 & 라이브러리</p>
</blockquote>
<ul>
<li>Keras : 오픈 소스 신경망 라이브러리</li>
<li>BeautifulSoup : HTML 데이터 parsing 라이브러리</li>
<li>Matplotlib : 시각화 라이브러리</li>
<li>PyQt5 : GUI 개발 프레임워크 </li>
</ul>
<blockquote> 
<p> IDE</p>
</blockquote>
<ul>
<li>Pycharm</li>
</ul>

## 2. 패키지 구조
<p><img src="md/3.PNG" alt="Alt"></p>
AvgGraph.py : 그래프 생성 클래스<br>
FinClawer.py : 네이버 금융정보 크롤링 클래스<br>
FinLearning.py : 인공지능 다중분류 클래스 <br>
StockStorterMain.py : GUI 생성을 담당하고 Main메소드가 존재하는 클래스<br>
DeeplearningModel 폴더 : 학습데이터, 테스트데이터, 학습된 모델 존재<br>


## 3. 데이터 수집 & 데이터 분석
<p><img src="md/4.PNG" alt="Alt"></p>
<hr>
<p><img src="md/result.PNG" alt="Alt"></p>
영웅문HTS에서 제공한 주식 분류별 포트폴리오 데이터를 활용하였습니다.
부채비율, 시가 배당률, 시가총액 세 값에서 유의미한 결과를 내는 것을 Matplotlib 시각화 분석으로 확인하였습니다.
데이터 전처리과정으로서 주식 이름, 주식 코드, 현재값과 같이 분류에 영향을 전혀 주지 않는 데이터 칼럼은 학습에서 제외하였습니다.

## 4.  모델 구축 & 모델검증
<p><img src="md/6.PNG" alt="Alt"></p>
여러 하이퍼 파라미터와 손실함수을 조합했을 때, 위와 같은 노드구성과 crossentropy 손실함수를 사용했을 때 결과값이 가장 좋았기에 위와 같은 구성을 사용하였습니다. 
<hr>
<p><img src="md/5.PNG" alt="Alt"></p>

## 5.  주요 기능

### 5-1.  종목 크롤링 & 종목 평균치 그래프 비교
<p><img src="md/1.gif" alt="Alt"></p>
<hr>

### 5-2.  주식 다중분류
<p><img src="md/2.gif" alt="Alt"></p>

## 6. 한계점 & 추후개발 과제
삼중분류로 개발했던 이전 버전에서는 다중분류의 정확도가 꽤나 높았으나 사중분류 문제로 넘어가니, 배당을 지급하지 않음에도, 우량한 회사를 중심으로 배당주로 인식하는 등 분류가 의도와 달리 이루어지지 않는 현상이 발행하였습니다.  AI 분류의 정확도를 높히고 여러가지 AI 분석기능을 추가하여 웹플랫폼으로 이식하는 것이 것이 추후과제 목표입니다.
