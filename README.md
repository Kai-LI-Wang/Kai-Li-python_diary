# Asset allocation for Stock Portfolio  

股票投資組合算法主要是來自於 Markowits 的 Modern Porfolio Theory(MPT), 目的是為了找出能最大化夏普比率(sharpe ratio)的投資組合權重, 夏普比率所代表的是1單位的風險能創造出多少報酬, 當夏普比率是越高, 代表者相同風險下的報酬就會越高, 理論上創造出最大的夏普比率的投資權重是風險與報酬最完美的投資組合 

## Steps:

### S1. 首先，計算每隻股票的標準差,並轉置成矩正
- Standard Deviation(SD) - 公式(1)

![](https://i.imgur.com/11QKQVU.png)
### S2. 再計算covariance 矩正
- Covariance Matrix - 公式(2)

![](https://i.imgur.com/HHAfUtE.png)
### S3. 並將 covariance 矩正除上標準差來獲得 correlation 矩正
- Correlation Matrix - 公式(3)

![](https://i.imgur.com/syr2jq8.png)
### S4. 利用correlation matrix 來計算投資組合標準差
- Standard Deviation of Portfolio - 公式(4)

![](https://i.imgur.com/Nq86N23.png)

### S5. 計算投資組合預期報酬
- Expected Return of Portfolio - 公式(4)

![](https://i.imgur.com/2PKM7k4.png)

### S6. 獲得預期報酬與投資組合標準差即可計算夏普比率（無風險利率假設為 30年treasury yield） 
- Sharpe Ratio - 公式(5)

![](https://i.imgur.com/cob2R7e.png)

### S7. 最後, 隨機模擬投資組合權重10000次並從中挑出夏普值最高的投資組合


## Getting Started 



## Running the test 






