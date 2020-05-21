# Pairs Trading 
## 概念
一般來說在建立投資組合的時候會選擇correlation 負相關的兩個資產來達到避險效果, 因為負相關的資產價格的移動方向正好相反, 當其中一個資產下跌另一個就會上漲，而conintegration 則是會解釋兩個資產之間的價格從長期來看是否會回到平均, 當cointegration 越高的時候, 會有越高的機會價格會回到平均, 也就是價格會屬於stationary, 雖然correlation 和 cointegration 看起來很相似, 但是兩者的概念並不相同, 有可能兩個資產的價格是correlated 但是卻不是 cointegrated(見下圖）, 下圖中兩個價格約分越開, 一個像上移動, 另一個向下移動, 兩者呈現負相關, 但是並沒有回到平均, 所以兩者並沒有cointegrated

![](https://i.imgur.com/HnknX2D.png)

在建立金融預測模型時, stationarity 是很關鍵的要素, Pairs Trading 就是建立於這個概念之上的套利交易方式, 本文中是利用兩個價格之間的比率來找出價格比率相對價格過高或價格過低的資產並將兩者反向對做沖銷價格波動以達到避險效果


## 作法
先去 wiki 擷取sp500的ticker, 並隨機選取50個ticker並將其分為n(n-1)/2個組合進行cointegration測試, 將測試結果為cointegrated的組合中的兩個資產(x,y)相除以計算價格比率(x/y), 再來計算價格比率的移動平均線, 並計算將移動平均線的 Z Score, 此目的為找出異常偏離平均的價格, 當價格比率過高代表資產x過大或資產y過小, 此時即可做空x 與作多y, 因為價格比率最終會返回平均 

## 理論
本文中使用python 模組 statsmodels.tsa.stattools 中的 coint函數, 此函數主要是使用 augmented Engle-Granger two-step cointegration test, 這個test是先計算回歸模型的residual, 再將residual與自身lag進行回歸並利用t-test再檢視residual 是否為stationary, 如果是即為cointegrated

