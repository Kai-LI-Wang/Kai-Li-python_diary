# Pairs Trading 
## 概念
一般來說在建立投資組合的時候會選擇correlation 負相關兩個資產已達到避險效果, 而conintegration 則是會解釋兩個資產之間的價格從長期來看是否會回到平均, 
當cointegration 越高的時候, 會有越高的機會價格會回到平均, 也就是價格會屬於stationary, 在建立金融預測模型時, stationarity 是很關鍵的要素, Pairs 
Trading 就是建立於這個概念之上的避險交易方式, 本文中是利用兩個價格之間的比率來找出價格比率相對價格過高或價格過低的資產並將兩者反向對做沖銷價格波動
已達到避險效果


