from binance.client import Client
from binance.enums import HistoricalKlinesType
from binanceapikeys import api_key,api_secret
from datetime import date
import yfinance as yf
from dateutil.relativedelta import relativedelta
import pandas as pd
import numpy as np
from scipy.stats import pearsonr
import matplotlib.pyplot as plt


# variables
enddate = date.today()
monthsbefore = 12
startdate = enddate - relativedelta(months=12)
yahooticker = "GBTC"
binanceticker = "BTCUSDT"

client = Client(api_key, api_secret)

hist = yf.Ticker(yahooticker).history(start=startdate,end=enddate,period="1d")
hist = hist[['Close']]
idx = pd.date_range(startdate,enddate)
df1 = hist.reindex(idx,fill_value = np.nan)
df1 = df1.ffill().fillna(hist['Close'].iloc[0])

klines = client.get_historical_klines(binanceticker,'1d',startdate.strftime("%Y-%m-%d"),klines_type=HistoricalKlinesType.FUTURES)
df2 = pd.DataFrame([(pd.to_datetime(day[0],unit='ms'),float(day[4])) for day in klines],columns=['Date','Price'])
df2 = df2.set_index('Date')

corr, _ = pearsonr(df1['Close'], df2['Price'])
print('Pearsons correlation: %.3f between %s and %s for %i months(s)' % (corr,yahooticker,binanceticker,monthsbefore) )

fig, ax1 = plt.subplots()
ax1.plot(df1,color='blue')
ax1.set_ylabel(yahooticker, color='blue')
ax2 = ax1.twinx()
ax2.plot(df2, 'red')
ax2.set_ylabel(binanceticker, color='red')
plt.tight_layout()
plt.show()