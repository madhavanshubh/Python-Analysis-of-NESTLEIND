import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader as web

df = pd.read_excel('T_bill_2019_2020_Daily.xlsx',index_col=0) 

df_Weekly  = df.resample('W-FRI').ffill().apply(lambda x: x*365/52).shift(-1)
df_Monthly = df.resample('M').ffill().apply(lambda x: x*365/12)

df_Weekly.ix[-2,'T-Bill Return% (Daily)']=0.0825
df_Weekly.drop(df_Weekly.tail(1).index,inplace=True) 
df_Weekly.drop(df_Weekly.head(1).index,inplace=True) 
df_Monthly.drop(df_Monthly.head(1).index,inplace=True) 
                                #cleaning part which exceeds time period or is NaN i.e first and last row

df_Weekly.columns=['Weekly']
df_Monthly.columns=['Monthly'] 
                                #changing column names     

nestle_Next = pd.read_excel('Futures Next Month.xlsx',index_col=0)
                                #reading relevant excel files

nestle_Next=nestle_Next.drop_duplicates()
                                #removing duplicate rows (cleaning data to make resampling feasible)

nestle_Next['Daily Return'] = nestle_Next['Settle Price'].pct_change(1)
nestle_Next_Weekly  = nestle_Next['Settle Price'].resample('W-FRI').ffill().pct_change()   
nestle_Next_Monthly = nestle_Next['Settle Price'].resample('M').ffill().pct_change()    
                                


nestle_Next_Weekly.drop(nestle_Next_Weekly.tail(3).index,inplace=True) 
                                #cleaning data to ensure it works with weekly t-bill dataframe   

nestle_Next_Monthly.drop(nestle_Next_Monthly.head(1).index,inplace=True) 
nestle_Next_Monthly.drop(nestle_Next_Monthly.tail(1).index,inplace=True) 
                                #matching indices

df['index1'] = df.index
nestle_Next['index1']=nestle_Next.index
days = pd.merge_ordered(nestle_Next, df,on='index1', fill_method='ffill')
days['Daily Return']=days['Daily Return']*100
days['Daily Excess']=days['Daily Return']-days['T-Bill Return% (Daily)']
                                 #cleaning data & forward filling to ensure it works with daily t-bill dataframe   

weeks=pd.DataFrame(columns=['Weekly Returns','Weekly TBill','Weekly Excess'])
weeks['Weekly Returns']=nestle_Next_Weekly*100
weeks['Weekly TBill']=df_Weekly['Weekly']
weeks['Weekly Excess']=weeks['Weekly Returns']-weeks['Weekly TBill']


months=pd.DataFrame(columns=['Monthly Returns','Monthly TBill','Monthly Excess'])
months['Monthly Returns']=nestle_Next_Monthly*100
months['Monthly TBill']=df_Monthly['Monthly']
months['Monthly Excess']=months['Monthly Returns']-months['Monthly TBill']

days['Daily Excess'].plot(kind='line',title='Line Graph for Daily Excess Returns')
plt.show()


weeks['Weekly Excess'].plot(kind='line',title='Line Graph for Weekly Excess Returns')
plt.show()

months['Monthly Excess'].plot(kind='line',title='Line Graph for Monthly Excess Returns')
plt.show()
