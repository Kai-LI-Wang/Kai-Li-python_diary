import matplotlib.pyplot as plt
import datetime as dt
import pandas_datareader.data as pdr
import pandas as pd 
import numpy as np 


class portfolio():
    def __init__(self, num_stock ,num_simulation,tickers,start,end,rf ):
        self.num_stock = num_stock
        self.num_simulation = num_simulation
        self.num_simulate = np.arange(self.num_simulation) 
        self.tickers = tickers
        self.start = start 
        self.end = end 
        self.df_close = self.get_stock_price()
        self.df_excess, self.df_return = self.excess_return()
        self.std_array = self.std_each_stock()
        self.std_mat = self.std_matrix()
        self.covariance_matrix = self.variance_covariance_matrix()
        self.correlation_mat = self.correlation_matrix()
        self.init_weights = self.weights_simulation()
        self.rf = rf
        self.sp500 = self.expected_ret_sp500()
        
    def get_stock_price(self):  
        start = self.start 
        end = self.end 
        df_close = pd.DataFrame(columns = self.tickers)
        for i in self.tickers: 
            df = pdr.DataReader(i,'yahoo',start,end)
            df_close[i]=df['Adj Close']
        return df_close 
    
    
    def stock_price_visualisation(self):
        tickers = self.tickers
        df_close = self.df_close
        fig = plt.figure(figsize=(10, 6))
        ax1 = fig.add_subplot(321)
        ax2 = fig.add_subplot(322)
        ax3 = fig.add_subplot(323)
        ax4 = fig.add_subplot(324)
        ax1.plot(df_close[tickers[0]])
        ax1.set_title(tickers[0])
        ax2.plot(df_close[tickers[1]])
        ax2.set_title(tickers[1])
        ax3.plot(df_close[tickers[2]])
        ax3.set_title(tickers[2])
        ax4.plot(df_close[tickers[3]])
        ax4.set_title(tickers[3])
        plt.tight_layout()
        plt.show()
        
    def excess_return(self):
        df_excess = pd.DataFrame([])
        df_return = pd.DataFrame([])
        for ticker in self.tickers:
            df_return[ticker] = np.log(self.df_close[ticker]).diff()
        #         df_return[ticker] = df_close[ticker].pct_change()            
            df_excess[ticker] = [(i - df_return[ticker].mean(axis = 0)) for i in df_return[ticker].values] 
        df_return.dropna(inplace = True)
        df_excess.dropna(inplace = True)
        return df_excess, df_return 
    
    def variance_covariance_matrix(self):   
        n = self.df_close.shape[0]
        covariance_matrix = (np.dot((np.array(self.df_excess)/n).T, np.array(self.df_excess))) #(df.shape[0],ticker).T(df.shape[0],ticker) = (ticker,ticker)
        return covariance_matrix #(4,4)
    
    def std_each_stock(self):
        std = []
        for ticker in self.tickers: 
            a = np.std(np.array(self.df_return[ticker])) 
            std.append(a)
        std_array = np.array(std).reshape(len(self.tickers),1)
        return std_array 
        
    def std_matrix(self):
        std_mat = np.dot(self.std_array, self.std_array.T) #(4,1)(4,1).T = (4,4)
        return std_mat #(stocks, stocks)
    
    
    def correlation_matrix(self):
        correlation_mat = self.covariance_matrix/self.std_mat #(4,4)/(4,4)
        return correlation_mat #(4,4)
    
    
    def weights_simulation(self):
        b =np.random.randint(10, size = self.num_stock)
        init_weights = np.array([j/np.sum(b) for j in b]).reshape(self.num_stock,1)  #(4,1)  
        return init_weights
    
    def portfolio_risk(self, weights): #Portfolio Variance = Sqrt (Transpose (Wt.SD) * Correlation Matrix * Wt. SD)
        port_variance = np.dot(np.dot(weights.T, self.correlation_mat), weights) #{[(4,1).T(4,4) = (1,4)], (4,1)} = (1,1)
        port_std = np.sqrt(port_variance[0][0])
        return port_std #(1,1) 
    
    
    def portfolio_return(self,weights):
        average_return_stock ={}
        list_avg_return = []
        avg_return = np.array([])
        for i in self.df_return.columns:
            average_return_stock[i] = self.df_return[i].mean() 
            list_avg_return.append(average_return_stock[i])
        avg_return = np.array(list_avg_return).reshape(1,len(self.df_return.columns))
        expected_return = np.sum(avg_return*weights.T) # (1, ticker)(4, 1).T = (df.shape, ticker)
        return expected_return
    
    def find_current_rf_rate(self):
    
        df = pdr.DataReader('DGS10','fred', start = self.end, end = self.end )
        for i in range(30):
            if df.empty:
                end = self.end + dt.timedelta(-1) 
                df = pdr.DataReader('DGS10','fred', start = end, end = end )
            else:
                print("the US 10 year treasury bond yield is:", df.values)
                break 
        return df.values[0][0]
    
    def Find_Sharpe_Ratio(self): # (average return - rf ) /std 
        column = ['sharpe','expected_return', 'port_risk']  + ['w1']+['w2']+['w3']+['w4']
        df_risk_return = pd.DataFrame(0, columns = column,index=self.num_simulate )
        for i in range(self.num_simulation):
            weights = self.weights_simulation()
            port_std = self.portfolio_risk(weights)
            expected_return = self.portfolio_return(weights)
            weight = list(weights)#(4,1)
            sharpe = (expected_return - self.rf)/port_std #[(1,1) - (1,1)]/(1,1)        
            df_risk_return.iloc[i,0] = sharpe
            df_risk_return.iloc[i,1] = expected_return
            df_risk_return.iloc[i,2] = port_std
            df_risk_return.iloc[i,3] = weight[0]
            df_risk_return.iloc[i,4] = weight[1]
            df_risk_return.iloc[i,5] = weight[2]
            df_risk_return.iloc[i,6] = weight[3]
        index = df_risk_return['sharpe'].idxmax(axis = 0)
        max_sharpe_port = df_risk_return.iloc[index]
        return df_risk_return, max_sharpe_port
    
    
    def expected_ret_sp500(self):
        df = pdr.DataReader('^GSPC','yahoo', start = self.start, end = self.end )
        return_sp500 = np.log(df).diff()
        avg_return_sp = return_sp500['Adj Close'].mean()
        return avg_return_sp
    
    
    
    
        
        
        
        
        
        
        
        
        
        
    
