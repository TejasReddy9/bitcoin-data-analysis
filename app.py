# 
# 
# ##########################
# Need to organize graphs more, regarding labels, and some plot size stuff
# 
# 
# 
# 
# 
# 

import urllib
import json
import pandas as pd 
import numpy as np 

import tkinter as tk 
from tkinter import ttk

import matplotlib
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
from mpl_finance import candlestick_ohlc
matplotlib.use("TkAgg")   # Back-end of matplotlib

from matplotlib import pyplot as plt 

# Canvas
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
# from matplotlib.figure import Figure
import matplotlib.animation as animation 
from matplotlib import style
style.use("ggplot")

WARNING_FONT = ("Helvetica Neue", 32)
MAIN_FONT = ("Helvetica Neue", 24)
DESCRIPTION_FONT = ("Helvetica Neue", 16)

DarkColor = "#00A3E0"
LightColor = "#183A54" 

Exchange = "BTC-e"
ForceUpdateHelper = 1000
ProgramName = "btce"

ResampleSize = "15Min"
DataPace = "tick"
CandleWidth = "0.008"

TopIndicator = "none"
MainIndicators = "none"
BottomIndicator = "none"
EMAs = []
SMAs = []

ChartLoaded = True
RefreshRate = 1000
PaneCount = 1 


# fig = Figure()
fig = plt.figure()
# a = fig.add_subplot(1,1,1)


# 
# 
# 	Animate function
# 
# 
def animate(i):
	# pass
	global RefreshRate
	global ForceUpdateHelper
	global PaneCount


	def computeMACD(price_data, slow=26, fast=12, location = "bottom"):

		values = { "key":1, "prices":price_data }

		url = "http://www.seaofbtc.com/api/indicator/macd"
		dataForRequest = urllib.parse.urlencode(values)
		dataForRequest = dataForRequest.encode("utf-8")
		request = urllib.request.Request(url, dataForRequest)
		data = urllib.request.urlopen(request)
		data = data.read()
		data = str(data).replace("b",'').replace("[",'').replace("]",'').replace("'",'')
		split = data.split("::")

		macd = split[0]
		ema9 = split[1]
		hist = split[2]

		macd = macd.split(", ")
		ema9 = ema9.split(", ")
		hist = hist.split(", ")

		macd = [float(i) for i in macd]
		ema9 = [float(i) for i in ema9]
		hist = [float(i) for i in hist]


		if location == "top":

			try:

				a4.plot(OHLC["mpldates"], macd, DarkColor, linewidth=2)
				a4.plot(OHLC["mpldates"], ema9, LightColor, linewidth=1)
				a4.fill_between(OHLC["mpldates"], hist, 0, alpha=0.5, facecolor = DarkColor, edgecolor = DarkColor) 
				a4.set_ylabel("MACD")

			except Exception as e:
				print("Error in MACD Indicator(top location) due to:", str(e))
				TopIndicator = "none"

		if location == "bottom":

			try:

				a3.plot(OHLC["mpldates"], macd, DarkColor, linewidth=2)
				a3.plot(OHLC["mpldates"], ema9, LightColor, linewidth=1)
				a3.fill_between(OHLC["mpldates"], hist, 0, alpha=0.5, facecolor = DarkColor, edgecolor = DarkColor) 
				a3.set_ylabel("MACD")

			except Exception as e:
				print("Error in MACD Indicator(bottom location) due to:", str(e))
				BottomIndicator = "none"











	def rsiIndicator(price_data, location = "top"):
		try:

			if location == "top":
				values = { "key":1, "prices":price_data, "periods":TopIndicator[1]}
			if location == "bottom":
				values = { "key":1, "prices":price_data, "periods":BottomIndicator[1]}

			url = "http://www.seaofbtc.com/api/indicator/rsi"
			dataForRequest = urllib.parse.urlencode(values)
			dataForRequest = dataForRequest.encode("utf-8")
			request = urllib.request.Request(url, dataForRequest)
			data = urllib.request.urlopen(request)
			data = data.read()
			# data = data[1:-1]
			# data = data.split(", ")
			# rsidata = []
			# for i in data:
			# 	if i != "nan":
			# 		rsidata.append(float(i))
			data = str(data).replace("b",'').replace("[",'').replace("]",'').replace("'",'')
			data = data.split(", ")
			rsidata = [float(i) for i in data]

			print(len(OHLC["mpldates"]), len(rsidata))


			if location == "top":
				a4.plot_date(OHLC["mpldates"], rsidata, LightColor, label = "RSI")
				a4.set_ylabel("RSI("+str(TopIndicator[1])+" periods)")

			if location == "bottom":
				a3.plot_date(OHLC["mpldates"], rsidata, LightColor, label = "RSI")
				a3.set_ylabel("RSI("+str(TopIndicator[1])+" periods)")

		except Exception as e:
			print("Error in RSI data acquisition due to:", str(e))




	if ChartLoaded == True:
		if PaneCount == 1:
			if DataPace == "tick":
				try:
					if Exchange == "BTC-e":
						# pass

						a = plt.subplot2grid((6,4), (0,0), rowspan = 5, colspan = 4)
						a2 = plt.subplot2grid((6,4), (5,0), rowspan = 1, colspan = 4, sharex = a)


						datalink = "https://wex.nz/api/3/trades/btc_usd?limit=1000"
						data = urllib.request.urlopen(datalink)  # in bytes
						data = data.read().decode("utf-8")  # decoded from bytes
						data = json.loads(data)
						data = data["btc_usd"]
						df = pd.DataFrame(data)

						df["datestamp"] = np.array(df["timestamp"]).astype("datetime64[s]")
						allDates = df["datestamp"].tolist()

						# matplotlib doesn't recognize unix timestamp
						buys = df[df["type"] == "bid"]
						sells = df[df["type"] == "ask"]
						if len(buys) > len(sells):
							x = len(buys) - len(sells)
							buys = buys[:-x]
						elif len(buys) < len(sells):
							x = len(sells) - len(buys)
							sells = sells[:-x]

						# buys["datestamp"] = np.array(buys["timestamp"]).astype("datetime64[s]")
						buyingDates = buys["datestamp"].tolist()
						
						# sells["datestamp"] = np.array(sells["timestamp"]).astype("datetime64[s]")
						sellingDates = buys["datestamp"].tolist()

						volume = df["amount"].apply(float).tolist()
						buys_price_data = buys["price"].apply(float).tolist()
						sells_price_data = sells["price"].apply(float).tolist()

						a.clear()
						a.plot_date(buyingDates, buys_price_data, DarkColor, label = "buys")
						a.plot_date(sellingDates, sells_price_data, LightColor, label = "sells")
						a2.fill_between(allDates, 0, volume, facecolor = LightColor)
						a.xaxis.set_major_locator(mticker.MaxNLocator(5))
						a.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M:%S"))
						plt.setp(a.get_xticklabels(), visible = False)
 
						a.legend(bbox_to_anchor = (0, 1.02, 1, 0.102), loc = 3, ncol = 2, borderaxespad = 0)  

						title = "WEX Bitcoin (BTCUSD)Prices\nLatest Price: $" + str(df["price"][0])
						a.set_title(title)

					elif Exchange == "Bitstamp":

						a = plt.subplot2grid((6,4), (0,0), rowspan = 5, colspan = 4)
						a2 = plt.subplot2grid((6,4), (5,0), rowspan = 1, colspan = 4, sharex = a)


						datalink = "https://www.bitstamp.net/api/transactions?limit=1000"
						data = urllib.request.urlopen(datalink)  # in bytes
						data = data.read().decode("utf-8")  # decoded from bytes
						data = json.loads(data)
						df = pd.DataFrame(data)

						df["datestamp"] = np.array(df["date"].apply(int)).astype("datetime64[s]")
						allDates = df["datestamp"].tolist()

						# matplotlib doesn't recognize unix timestamp
						# buys = df[df["type"] == "bid"]
						# sells = df[df["type"] == "ask"]
						# if len(buys) > len(sells):
						# 	x = len(buys) - len(sells)
						# 	buys = buys[:-x]
						# elif len(buys) < len(sells):
						# 	x = len(sells) - len(buys)
						# 	sells = sells[:-x]

						# buys["datestamp"] = np.array(buys["timestamp"]).astype("datetime64[s]")
						# buyingDates = buys["datestamp"].tolist()
						  
						# sells["datestamp"] = np.array(sells["timestamp"]).astype("datetime64[s]")
						# sellingDates = buys["datestamp"].tolist()

						volume = df["amount"].apply(float).tolist()
						price_data = df["price"].apply(float).tolist()

						a.clear()
						a.plot_date(allDates, price_data, DarkColor, label = "sales")
						# a.plot_date(buyingDates, buys["price"], DarkColor, label = "buys")
						# a.plot_date(sellingDates, sells["price"], LightColor, label = "sells")
						a2.fill_between(allDates, 0, volume, facecolor = LightColor)
						a.xaxis.set_major_locator(mticker.MaxNLocator(5))
						a.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M:%S"))
						plt.setp(a.get_xticklabels(), visible = False)

						a.legend(bbox_to_anchor = (0, 1.02, 1, 0.102), loc = 3, ncol = 2, borderaxespad = 0)  

						title = "Bitstamp (BTCUSD)Prices\nLatest Price: $" + str(df["price"][0])
						a.set_title(title)

					elif Exchange == "Bitfinex":

						a = plt.subplot2grid((6,4), (0,0), rowspan = 5, colspan = 4)
						a2 = plt.subplot2grid((6,4), (5,0), rowspan = 1, colspan = 4, sharex = a)


						datalink = "https://api.bitfinex.com/v1/trades/btcusd?limit=1000"
						data = urllib.request.urlopen(datalink)  # in bytes
						data = data.read().decode("utf-8")  # decoded from bytes
						data = json.loads(data)
						df = pd.DataFrame(data)

						df["datestamp"] = np.array(df["timestamp"]).astype("datetime64[s]")
						allDates = df["datestamp"].tolist()

						# matplotlib doesn't recognize unix timestamp
						buys = df[df["type"] == "buy"]
						sells = df[df["type"] == "sell"]
						if len(buys) > len(sells):
							x = len(buys) - len(sells)
							buys = buys[:-x]
						elif len(buys) < len(sells):
							x = len(sells) - len(buys)
							sells = sells[:-x]

						# buys["datestamp"] = np.array(buys["timestamp"]).astype("datetime64[s]")
						buyingDates = buys["datestamp"].tolist()
						
						# sells["datestamp"] = np.array(sells["timestamp"]).astype("datetime64[s]")
						sellingDates = buys["datestamp"].tolist()

						volume = df["amount"].apply(float).tolist()
						buys_price_data = buys["price"].apply(float).tolist()
						sells_price_data = sells["price"].apply(float).tolist()

						a.clear()
						a.plot_date(buyingDates, buys_price_data, DarkColor, label = "buys")
						a.plot_date(sellingDates, sells_price_data, LightColor, label = "sells")
						a2.fill_between(allDates, 0, volume, facecolor = LightColor)
						a.xaxis.set_major_locator(mticker.MaxNLocator(5))
						a.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M:%S")) 
						plt.setp(a.get_xticklabels(), visible = False)

						a.legend(bbox_to_anchor = (0, 1.02, 1, 0.102), loc = 3, ncol = 2, borderaxespad = 0)  

						title = "Bitfinex (BTCUSD)Prices\nLatest Price: $" + str(df["price"][0])
						a.set_title(title)

					elif Exchange == "Huobi":

						a = plt.subplot2grid((6,4), (0,0), rowspan = 6 , colspan = 4)
						datalink = "http://www.seaofbtc.com/api/basic/price?key=1&tf=1d&exchange=" + ProgramName
						data = urllib.request.urlopen(datalink)
						data = data.read().decode("utf-8")
						data = json.loads(data)

						df = pd.DataFrame({ "timestamp": data[0], "price": data[1] })

						df["datestamp"] = np.array(df["timestamp"]).astype("datetime64[s]")
						allDates = df["datestamp"].tolist()

						# df["datetime"] = df["datetime"].apply(lambda date: mdates.date2num(date.to_pydatetime()))

						df = df.set_index("datestamp")
						price_data = df["price"].apply(float).tolist()


						a.clear()
						a.plot_date(allDates, price_data, DarkColor, label = "sales")
						# a2.fill_between(df["datetime"][-4500:], 0, df["volume"][-4500:], facecolor = LightColor)
						a.xaxis.set_major_locator(mticker.MaxNLocator(5))
						a.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M:%S"))
						# plt.setp(a.get_xticklabels(), visible = False)

						# a.legend(bbox_to_anchor = (0, 1.02, 1, 0.102), loc = 3, ncol = 2, borderaxespad = 0)  

						title = "Huobi (BTCUSD)Prices\nLatest Price: $" + str(df["price"][0])
						a.set_title(title)


				except Exception as e:
					print("Error in tick data animation of",Exchange,"due to:",str(e))

			else:
				if ForceUpdateHelper > 12:
					try:

						if Exchange == "Huobi":

							if TopIndicator != "none":
								a1 = plt.subplot2grid((6,4), (1,0), rowspan = 5, colspan = 4)
								a2 = plt.subplot2grid((6,4), (0,0), rowspan = 1, colspan = 4, sharex = a1)
							else:
								a1 = plt.subplot2grid((6,4), (0,0), rowspan = 6, colspan = 4)

						else:

							if TopIndicator != "none" and BottomIndicator != "none":
								a1 = plt.subplot2grid((6,4), (1,0), rowspan = 3, colspan = 4)  # Main Graph
								a2 = plt.subplot2grid((6,4), (4,0), rowspan = 1, colspan = 4, sharex = a1)  # Volume
								a3 = plt.subplot2grid((6,4), (5,0), rowspan = 1, colspan = 4, sharex = a1)  # Bottom Indicator
								a4 = plt.subplot2grid((6,4), (0,0), rowspan = 1, colspan = 4, sharex = a1)  # Top Indicator
							elif TopIndicator != "none":
								a1 = plt.subplot2grid((6,4), (1,0), rowspan = 4, colspan = 4)  # Main Graph
								a2 = plt.subplot2grid((6,4), (5,0), rowspan = 1, colspan = 4, sharex = a1)  # Volume
								a4 = plt.subplot2grid((6,4), (0,0), rowspan = 1, colspan = 4, sharex = a1)  # Top Indicator
							elif BottomIndicator != "none":
								a1 = plt.subplot2grid((6,4), (0,0), rowspan = 4, colspan = 4)  # Main Graph
								a2 = plt.subplot2grid((6,4), (4,0), rowspan = 1, colspan = 4, sharex = a1)  # Volume
								a3 = plt.subplot2grid((6,4), (5,0), rowspan = 1, colspan = 4, sharex = a1)  # Bottom Indicator
							else:
								a1 = plt.subplot2grid((6,4), (0,0), rowspan = 5, colspan = 4)  # Main Graph
								a2 = plt.subplot2grid((6,4), (5,0), rowspan = 1, colspan = 4, sharex = a1)  # Volume

						datalink = "http://www.seaofbtc.com/api/basic/price?key=1&tf=" + DataPace + "&exchange=" + ProgramName
						data = urllib.request.urlopen(datalink)
						data = data.read().decode("utf-8")
						data = json.loads(data)

						df = pd.DataFrame({ "timestamp": data[0], "price": data[1], "volume": data[2] })
						df["datestamp"] = np.array(df["timestamp"]).astype("datetime64[s]")
						allDates = df["datestamp"].tolist()
						# allDates = np.array(df["timestamp"]).astype("datetime64[s]").tolist()

						df.set_index("datestamp", inplace = True)

						OHLC = df["price"].resample(ResampleSize).ohlc()
						# OHLC.dropna(inplace = True)

						Vol = pd.DataFrame()
						Vol["volume"] = df["volume"].resample(ResampleSize).sum()
						# Vol.dropna(inplace = True)

						OHLC["datestamp"] = OHLC.index
						Vol["datestamp"] = Vol.index

						price_data = OHLC["close"].apply(float).tolist()
						OHLC["mpldates"] = OHLC["datestamp"].apply(lambda date: mdates.date2num(date.to_pydatetime()))
						Vol["mpldates"] = Vol["datestamp"].apply(lambda date: mdates.date2num(date.to_pydatetime()))
						# OHLC["datestamp"] = OHLC["datestamp"].apply(float).tolist()

						a1.clear()

						if MainIndicators != "none":

							for ma in MainIndicators:
								if ma[0] == "sma":
									# sma = pd.rolling_mean(OHLC["close"], ma[1])
									sma = OHLC["close"].rolling(ma[1]).mean()
									a1.plot(OHLC["datestamp"], sma, label = str(ma[1])+" SMA")

								elif ma[0] == "ema":
									pass
									######## Need FIX as pd.stats.moments.ewma has been moved to some other area in pandas
									# ewma = pd.stats.moments.ewma(OHLC["close"], ma[1])
									# a1.plot(OHLC["datestamp"], ewma, label = str(ma[1])+" EMA")

							a1.legend(loc=0)

						if TopIndicator[0] == "rsi":
							rsiIndicator(price_data, "top")
						elif TopIndicator == "macd":
							try:
								computeMACD(price_data, location = "top")
							except Exception as e:
								print("Error in MACD Top Indicator",str(e))

						if BottomIndicator[0] == "rsi":
							rsiIndicator(price_data, "bottom")
						elif BottomIndicator == "macd":
							try:
								computeMACD(price_data, location =  "bottom")
							except Exception as e:
								print("Error in MACD Bottom Indicator",str(e))



						csticks = candlestick_ohlc(a1, 
												OHLC[["mpldates", "open", "high", "low", "close"]].values, 
												width = float(CandleWidth), 
												colorup = LightColor, 
												colordown = DarkColor)

						a1.set_ylabel("Price")
						if Exchange != "Huobi":
							a2.fill_between(Vol["mpldates"], 0, Vol["volume"], facecolor = DarkColor)
							a2.set_ylabel("Volume")

						a1.xaxis.set_major_locator(mticker.MaxNLocator(3))
						a1.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M"))

						if Exchange != "Huobi":
							plt.setp(a1.get_xticklabels(), visible = False)
 
						if TopIndicator != "none":
							plt.setp(a4.get_xticklabels(), visible = False)

						if BottomIndicator != "none":
							plt.setp(a3.get_xticklabels(), visible = False)

						if DataPace != "none":
							title = "Exchange:{} - TimeFrame:{} - ResampleSize:{}\nLastPrice:{}".format(Exchange, DataPace, ResampleSize, OHLC["close"][-1])

						if TopIndicator != "none":
							a4.set_title(title)
						if BottomIndicator != "none":
							a3.set_title(title)

						ForceUpdateHelper = 0


					except Exception as e:
						print("Error in non-tick data animation due to:", str(e))
						ForceUpdateHelper = 2000

				else:
					ForceUpdateHelper+=1
# End of function: animate()


# 
# 
# 	Popup Messgae Function 
# 
#
def popupmsg(message):
	popup = tk.Tk()
	popup.wm_title("!")
	label = ttk.Label(popup, text = message, font = MAIN_FONT)
	label.pack(side = "top", fill = "x", pady=10)
	buttonOkay = ttk.Button(popup, text = "Okay", command = popup.destroy)
	buttonOkay.pack()
	popup.mainloop()
# End of function: popupmsg()


# 
# 
# 	Change exchange Function 
# 
#
def changeExchange(target, pn):
	global Exchange
	global ForceUpdateHelper
	global ProgramName

	Exchange = target
	ProgramName = pn
	ForceUpdateHelper = 2000
# End of function: changeExchange()



# 
# 
# 	Change Timeframe Function 
# 
#
def changeTimeFrame(tf):
	global DataPace
	global ForceUpdateHelper
	if tf == "7d" and ResampleSize == "1Min":
		popupmsg("Too much data choosen.\nChoose a smaller timeframe or higher OHLC Interval")
	else:
		DataPace = tf
		ForceUpdateHelper = 2000
# End of function: changeTimeFrame()


# 
# 
# 	Change Sample Size Function 
# 
#
def changeSampleSize(size, width):
	global ResampleSize
	global ForceUpdateHelper
	global CandleWidth
	if DataPace == "7d" and ResampleSize == "1Min":
		popupmsg("Too much data choosen.\nChoose a smaller timeframe or higher OHLC Interval")
	elif DataPace == "tick":
		popupmsg("You are currently viewing tick data, not OHLC.")
	else:
		ResampleSize = size
		ForceUpdateHelper = 2000
		CandleWidth = width
# End of function: changeSampleSize()


# 
# 
# 	Add Top Indicator function
# 
# 
def addTopIndicator(indicator):
	global TopIndicator
	global ForceUpdateHelper

	if DataPace == "tick":
		popupmsg("Indicators in tick data are not available.")
	elif indicator == "none":
		TopIndicator = indicator
		ForceUpdateHelper = 2000
	elif indicator == "rsi":
		rsiQ = tk.Tk()
		rsiQ.wm_title("Periods?")
		label = tk.Label(rsiQ, text = "How many periods do you want for each RSI calculation to consider?")
		label.pack(side = "top", pady=10)

		entryWidget = ttk.Entry(rsiQ)
		entryWidget.insert(0,14)
		entryWidget.pack()
		entryWidget.focus_set()

		def callback():
			global TopIndicator
			global ForceUpdateHelper

			periods = entryWidget.get()
			group = []
			group.append("rsi")
			group.append(int(periods))

			TopIndicator = group
			ForceUpdateHelper = 2000
			print("Set top indicator to", group)
			rsiQ.destroy()

		buttonSubmit = ttk.Button(rsiQ, text="Submit", width=10, command = callback)
		buttonSubmit.pack()
		rsiQ.mainloop()
	elif indicator == "macd":
		TopIndicator = "macd"
		ForceUpdateHelper = 2000
# End of function: addTopIndicator()


# 
# 
# 	Add Bottom Indicator function
# 
# 
def addBottomIndicator(indicator):
	global BottomIndicator
	global ForceUpdateHelper

	if DataPace == "tick":
		popupmsg("Indicators in tick data are not available.")
	elif indicator == "none":
		BottomIndicator = indicator
		ForceUpdateHelper = 2000
	elif indicator == "rsi":
		rsiQ = tk.Tk()
		rsiQ.wm_title("Periods?")
		label = tk.Label(rsiQ, text = "How many periods do you want for each RSI calculation to consider?")
		label.pack(side = "top", pady=10)

		entryWidget = ttk.Entry(rsiQ)
		entryWidget.insert(0,14)
		entryWidget.pack()
		entryWidget.focus_set()

		def callback():
			global BottomIndicator
			global ForceUpdateHelper

			periods = entryWidget.get()
			group = []
			group.append("rsi")
			group.append(int(periods))

			BottomIndicator = group
			ForceUpdateHelper = 2000
			print("Set bottom indicator to", group)
			rsiQ.destroy()

		buttonSubmit = ttk.Button(rsiQ, text="Submit", width=10, command = callback)
		buttonSubmit.pack()
		rsiQ.mainloop()
	elif indicator == "macd":
		BottomIndicator = "macd"
		ForceUpdateHelper = 2000
# End of function: addBottomIndicator()


# 
# 
# 	Add Main Indicator function
# 
# 
def addMainIndicator(indicator):
	global MainIndicators
	global ForceUpdateHelper

	if DataPace == "tick":
		popupmsg("Indicators in tick data are not available.")
	elif indicator != "none":
		if MainIndicators == "none":
			if indicator == "sma":
				smaQ = tk.Tk()
				smaQ.wm_title("Periods?")
				label = tk.Label(smaQ, text = "How many periods do you want for each SMA calculation to consider?")
				label.pack(side = "top", fill = "x", pady=10)

				entryWidget = ttk.Entry(smaQ)
				entryWidget.insert(0,10)
				entryWidget.pack()
				entryWidget.focus_set()

				def callback():
					global MainIndicators
					global ForceUpdateHelper

					MainIndicators = []
					periods = entryWidget.get()
					group = []
					group.append("sma")
					group.append(int(periods))
					MainIndicators.append(group)

					ForceUpdateHelper = 2000
					print("Set main indicator to", MainIndicators)
					smaQ.destroy()

				buttonSubmit = ttk.Button(smaQ, text="Submit", width=10, command = callback)
				buttonSubmit.pack()
				smaQ.mainloop()
			if indicator == "ema":
				emaQ = tk.Tk()
				emaQ.wm_title("Periods?")
				label = tk.Label(emaQ, text = "How many periods do you want for each EMA calculation to consider?")
				label.pack(side = "top", fill = "x", pady=10)

				entryWidget = ttk.Entry(emaQ)
				entryWidget.insert(0,10)
				entryWidget.pack()
				entryWidget.focus_set()

				def callback():
					global MainIndicators
					global ForceUpdateHelper

					MainIndicators = []
					periods = entryWidget.get()
					group = []
					group.append("ema")
					group.append(int(periods))
					MainIndicators.append(group)

					ForceUpdateHelper = 2000
					print("Set main indicator to", MainIndicators)
					emaQ.destroy()

				buttonSubmit = ttk.Button(emaQ, text="Submit", width=10, command = callback)
				buttonSubmit.pack()
				emaQ.mainloop()
		else:
			if indicator == "sma":
				smaQ = tk.Tk()
				smaQ.wm_title("Periods?")
				label = tk.Label(smaQ, text = "How many periods do you want for each SMA calculation to consider?")
				label.pack(side = "top", fill = "x", pady=10)

				entryWidget = ttk.Entry(smaQ)
				entryWidget.insert(0,10)
				entryWidget.pack()
				entryWidget.focus_set()

				def callback():
					global MainIndicators
					global ForceUpdateHelper

					# MainIndicators = []
					periods = entryWidget.get()
					group = []
					group.append("sma")
					group.append(int(periods))
					MainIndicators.append(group)

					ForceUpdateHelper = 2000
					print("Set main indicator to", MainIndicators)
					smaQ.destroy()

				buttonSubmit = ttk.Button(smaQ, text="Submit", width=10, command = callback)
				buttonSubmit.pack()
				smaQ.mainloop()
			if indicator == "ema":
				emaQ = tk.Tk()
				emaQ.wm_title("Periods?")
				label = tk.Label(emaQ, text = "How many periods do you want for each EMA calculation to consider?")
				label.pack(side = "top", fill = "x", pady=10)

				entryWidget = ttk.Entry(emaQ)
				entryWidget.insert(0,10)
				entryWidget.pack()
				entryWidget.focus_set()

				def callback():
					global MainIndicators
					global ForceUpdateHelper

					# MainIndicators = []
					periods = entryWidget.get()
					group = []
					group.append("ema")
					group.append(int(periods))
					MainIndicators.append(group)

					ForceUpdateHelper = 2000
					print("Set main indicator to", MainIndicators)
					emaQ.destroy()

				buttonSubmit = ttk.Button(emaQ, text="Submit", width=10, command = callback)
				buttonSubmit.pack()
				emaQ.mainloop()
	else:
		MainIndicators = "none"
# End of function: addMainIndicator()


#
#
# 	Load chart function
#
#
def loadChart(run):
	global ChartLoaded
	if run == "start":
		ChartLoaded = True
	elif run == "stop":
		ChartLoaded = False
# End of function: loadChart()


#
#
# 	Tutorial function: Cascading windows in a sense
#
#
def tutorial():

	def part2():
		tut.destroy() 	# kill present page

		def part3():
			tut2.destroy()

			tut3 = tk.Tk() 
			tut3.wm_title("Tutorial")
			label = tk.Label(tut3, text = "Part 3", font = MAIN_FONT)
			label.pack(side = "top", fill = "x", pady=10)
			buttonPart4 = tk.Button(tut3, text = "Quit", command = tut3.destroy)
			buttonPart4.pack(side = "top", fill = "x", pady=10)
			tut3.mainloop()

		tut2 = tk.Tk() 	# create new instead
		tut2.wm_title("Tutorial")
		label = tk.Label(tut2, text = "Part 2", font = MAIN_FONT)
		label.pack(side = "top", fill = "x", pady=10)
		buttonPart3 = tk.Button(tut2, text = "Go to part 3", command = part3)
		buttonPart3.pack(side = "top", fill = "x", pady=10)
		tut2.mainloop()

	tut = tk.Tk()
	tut.wm_title("Tutorial")
	label = tk.Label(tut, text = "Tutorial", font = MAIN_FONT)
	label.pack(side = "top", fill = "x", pady=10)
	buttonOverview = tk.Button(tut, text = "Overview of the Application", command = part2)
	buttonOverview.pack(side = "top", fill = "x", pady=10)
	tut.mainloop()
# End of function: tutorial()





# 
# 
# 	Class: Application
# 
# 
class Application(tk.Tk):

	def __init__(self, *args, **kwargs):

		tk.Tk.__init__(self, *args, **kwargs)
		tk.Tk.wm_title(self, "Application")

		container = tk.Frame(self)
		container.pack(side = "top", fill="both", expand = True)

		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		#### Menu bar
		menubar = tk.Menu(container)
		filemenu = tk.Menu(menubar)
		filemenu.add_command(label = "Save settings", command = lambda: popupmsg("Not supported!"))
		filemenu.add_separator()
		filemenu.add_command(label = "Exit", command = quit)
		menubar.add_cascade(label = "File", menu = filemenu)

		exchangeChoice = tk.Menu(menubar)
		exchangeChoice.add_command(label = "BTC-e", 
								command = lambda: changeExchange("BTC-e","btce"))
		exchangeChoice.add_command(label = "Bitfinex", 
								command = lambda: changeExchange("Bitfinex","bitfinex"))
		exchangeChoice.add_command(label = "Bitstamp", 
								command = lambda: changeExchange("Bitstamp","bitstamp"))
		exchangeChoice.add_command(label = "Huobi", 
								command = lambda: changeExchange("Huobi","huobi"))
		menubar.add_cascade(label = "Exchange", menu = exchangeChoice)

		dataTimeFrame = tk.Menu(menubar)
		dataTimeFrame.add_command(label = "Tick", 
								command = lambda: changeTimeFrame("tick"))
		dataTimeFrame.add_command(label = "1 Day", 
								command = lambda: changeTimeFrame("1d"))
		dataTimeFrame.add_command(label = "3 Day", 
								command = lambda: changeTimeFrame("3d"))
		dataTimeFrame.add_command(label = "1 Week", 
								command = lambda: changeTimeFrame("7d"))
		menubar.add_cascade(label = "Data Time Frame", menu = dataTimeFrame)

		OHLCInterval = tk.Menu(menubar)
		OHLCInterval.add_command(label = "Tick", 
							command = lambda: changeSampleSize("tick"))
		OHLCInterval.add_command(label = "1 Minute",
							command = lambda: changeSampleSize("1Min", 0.0005))
		OHLCInterval.add_command(label = "5 Minute",
							command = lambda: changeSampleSize("5Min", 0.003))
		OHLCInterval.add_command(label = "15 Minute",
							command = lambda: changeSampleSize("15Min", 0.008))
		OHLCInterval.add_command(label = "30 Minute",
							command = lambda: changeSampleSize("30Min", 0.016))
		OHLCInterval.add_command(label = "1 Hour",
							command = lambda: changeSampleSize("1H", 0.032))
		OHLCInterval.add_command(label = "3 Hour",
							command = lambda: changeSampleSize("3H", 0.096))
		menubar.add_cascade(label = "OHLC Interval", menu = OHLCInterval)

		topIndicatorMenu = tk.Menu(menubar)
		topIndicatorMenu.add_command(label = "None", 
							command = lambda: addTopIndicator("none"))
		topIndicatorMenu.add_command(label = "RSI", 
							command = lambda: addTopIndicator("rsi"))
		topIndicatorMenu.add_command(label = "MACD", 
							command = lambda: addTopIndicator("macd"))
		menubar.add_cascade(label = "Top Indicator", menu = topIndicatorMenu)


		mainIndicatorMenu = tk.Menu(menubar)
		mainIndicatorMenu.add_command(label = "None", 
							command = lambda: addMainIndicator("none"))
		mainIndicatorMenu.add_command(label = "SMA", 
							command = lambda: addMainIndicator("sma"))
		mainIndicatorMenu.add_command(label = "EMA", 
							command = lambda: addMainIndicator("ema"))
		menubar.add_cascade(label = "Main/Middle Indicator", menu = mainIndicatorMenu)


		bottomIndicatorMenu = tk.Menu(menubar)
		bottomIndicatorMenu.add_command(label = "None", 
							command = lambda: addBottomIndicator("none"))
		bottomIndicatorMenu.add_command(label = "RSI", 
							command = lambda: addBottomIndicator("rsi"))
		bottomIndicatorMenu.add_command(label = "MACD", 
							command = lambda: addBottomIndicator("macd"))
		menubar.add_cascade(label = "Bottom Indicator", menu = bottomIndicatorMenu)

		
		trademenu = tk.Menu(menubar)
		trademenu.add_command(label = "Manual Trading", 
							command = lambda: popupmsg("This isn't live yet!"))
		trademenu.add_command(label = "Automatic Trading",
							command = lambda: popupmsg("This isn't live yet!"))
		trademenu.add_separator()
		trademenu.add_command(label = "Quick Buy", 
							command = lambda: popupmsg("This isn't live yet!"))
		trademenu.add_command(label = "Quick Sell", 
							command = lambda: popupmsg("This isn't live yet!"))
		trademenu.add_separator()
		trademenu.add_command(label = "Setup Quick Buy/Sell", 
							command = lambda: popupmsg("This isn't live yet!"))
		menubar.add_cascade(label = "Trading", menu = trademenu)

		runmenu = tk.Menu(menubar)
		runmenu.add_command(label = "Resume", command = lambda: loadChart("start"))
		runmenu.add_command(label = "Pause", command = lambda: loadChart("stop"))
		menubar.add_cascade(label = "Run", menu = runmenu)

		helpmenu = tk.Menu(menubar)
		helpmenu.add_command(label = "Tutorial", command = tutorial)
		menubar.add_cascade(label = "Help", menu = helpmenu)


		tk.Tk.config(self, menu = menubar)


		self.frames = {}

		for F in (StartPage, BitcoinAppPage):

			frame = F(container, self)
			self.frames[F] = frame
			frame.grid(row=0, column=0, sticky = "nsew")

		self.show_frame(StartPage)
	# end __init__()

	def show_frame(self, controller):

		frame = self.frames[controller]
		frame.tkraise()
	# end show_frame()
# End of class: Application


# 
# 
# 	Class: Start Page 
# 
# 
class StartPage(tk.Frame):

	def __init__(self, parent, controller):

		tk.Frame.__init__(self, parent)
		labelHeading = ttk.Label(self, text = "Bitcoin Trading Application", font = MAIN_FONT)
		labelHeading.pack(pady=10, padx=10)

		labelDescription = tk.Label(self, text = "This is still a Beta version.\nDeveloped and maintained by K Tejas Reddy.\n2018.", 
										font = DESCRIPTION_FONT)
		labelDescription.pack(pady=10, padx=10)

		buttonAgree = ttk.Button(self, text = "Agree", 
									command = lambda: controller.show_frame(BitcoinAppPage))
		buttonAgree.pack()

		buttonDisagree = ttk.Button(self, text = "Disagree", 
										command = quit)
		buttonDisagree.pack()
	# end __init__()
# End of class: StartPage


# # 
# # 
# # 	Class: Details Page 
# # 
# # 
# class DetailsPage(tk.Frame):

# 	def __init__(self, parent, controller):

# 		tk.Frame.__init__(self, parent)
# 		labelHeading = tk.Label(self, text = "Details", font = MAIN_FONT)
# 		labelHeading.pack(pady=10, padx=10)

# 		buttonBackToStartPage = ttk.Button(self, text = "Back to Home", 
# 											command = lambda: controller.show_frame(StartPage))
# 		buttonBackToStartPage.pack()

# 		buttonToHelpPage = ttk.Button(self, text = "Help Page", 
# 											command = lambda: controller.show_frame(HelpPage))
# 		buttonToHelpPage.pack()
# 	# end __init__()
# # End of class: DetailsPage


# # 
# # 
# # 	Class: Help Page 
# # 
# # 
# class HelpPage(tk.Frame):

# 	def __init__(self, parent, controller):

# 		tk.Frame.__init__(self, parent)
# 		labelHeading = tk.Label(self, text = "Get some Help here", font = MAIN_FONT)
# 		labelHeading.pack(pady=10, padx=10)

# 		buttonToDetailsPage = ttk.Button(self, text = "Visit Details Page", 
# 											command = lambda: controller.show_frame(DetailsPage))
# 		buttonToDetailsPage.pack()

# 		buttonBackToStartPage = ttk.Button(self, text = "Back to Home", 
# 											command = lambda: controller.show_frame(StartPage))
# 		buttonBackToStartPage.pack()
# 	# end __init__()
# # End of class: HelpPage


# 
# 
# 	Class: Bitcoin App Page 
# 
# 
class BitcoinAppPage(tk.Frame):

	def __init__(self, parent, controller):

		tk.Frame.__init__(self, parent)
		labelHeading = tk.Label(self, text = "Graphs", font = MAIN_FONT)
		labelHeading.pack(pady=10, padx=10)

		buttonToDetailsPage = ttk.Button(self, text = "Back to Home Page", 
											command = lambda: controller.show_frame(StartPage))
		buttonToDetailsPage.pack()

		canvas = FigureCanvasTkAgg(fig, self)
		canvas.draw()
		canvas.get_tk_widget().pack(side = tk.TOP, fill = tk.BOTH, expand = True)

		toolbar = NavigationToolbar2Tk(canvas, self)
		toolbar.update()
		canvas._tkcanvas.pack(side = tk.TOP, fill = tk.BOTH, expand = True)
	# end __init__()
# End of class: Bitcoin App Page 




# 
# 
# 	 Run app
# 
#
app = Application()
app.geometry("1280x720")  # Application size
animation = animation.FuncAnimation(fig, animate, interval=2000)
app.mainloop()




