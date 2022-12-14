from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract

import threading
import time

class IBapi(EWrapper, EClient):
	def __init__(self):
		EClient.__init__(self, self)
		self.data = [] #Initialize variable to store candle

	def historicalData(self, reqId, bar):
		print(f'Time: {bar.date} Open:{bar.open} High: {bar.high} Low: {bar.low} Close: {bar.close} Volume:{bar.volume}')
		self.data.append([bar.date, bar.open, bar.high, bar.low, bar.close, bar.volume])
		
def run_loop():
	app.run()

app = IBapi()
app.connect('127.0.0.1', 7497, 123)

#Start the socket in a thread
api_thread = threading.Thread(target=run_loop, daemon=True)
api_thread.start()

time.sleep(1) #Sleep interval to allow time for connection to server

#Create contract object
eurusd_contract = Contract()
eurusd_contract.symbol = '700'
eurusd_contract.secType = 'STK'
eurusd_contract.exchange = 'SMART'
eurusd_contract.currency = 'HKD'

#Request historical candles
app.reqHistoricalData(1, eurusd_contract, '', '2 D', '1 hour', 'TRADES', 0, 2, False, [])

time.sleep(5) #sleep to allow enough time for data to be returned
app.disconnect()


#Working with Pandas DataFrames
import pandas

df = pandas.DataFrame(app.data, columns=['DateTime', 'Open', 'High', 'Low', 'Close'])
df['DateTime'] = pandas.to_datetime(df['DateTime'],unit='s') 
df.to_csv('EURUSD_Hourly.csv')  

print(df)