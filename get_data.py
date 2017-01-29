import datetime
import timeit
import io
import pandas as pd
import pandas_datareader.data as web
from parameters import parameters

def main_get_data(parameters):
	dfs = make_frames_wrapper(parameters=parameters)
	output = io.BytesIO()
	writer = pd.ExcelWriter(output, engine='xlsxwriter')
	for df in dfs:
		print(df.head)
		df_symbol = df['Symbol'].values[0]
		df.to_excel(writer,df_symbol)
	writer.close()
	output.seek(0)
	r = output.read()
	return r

def make_frames_wrapper(parameters):
	print(parameters)
	# prepare parameters
	start, end = make_date_objects(parameters['start_date'], parameters['end_date'])
	weights = [
		float_option(parameters['thirty_day_weight']), float_option(parameters['sixty_day_weight']), 
		float_option(parameters['ninety_day_weight']), float_option(parameters['one_eighty_day_weight'])
			]
	symbols = parameters['symbols']
	# make the API calls and build the dataframe
	frames = make_frames(symbols=symbols, start=start, end=end, weights=weights)
	return frames

def make_date_objects(*dates):
	date_objects = []
	for date in dates:
		print('date before split', date)
		date = [int(string) for string in date.split('/')]
		print('date after split', date)
		obj=datetime.date(date[2], date[0], date[1])
		print(date[2], date[0], date[1])
		date_objects.append(obj)
	return date_objects

def make_frames(symbols, start, end, weights):
	real_start = start - datetime.timedelta(days=400)
	frames = []
	for symbol in symbols:
		print(symbol)
		df = web.DataReader(symbol, 'yahoo', real_start, end)
		print(df.head)
		df = add_columns(df)
		df['Symbol'] = symbol
		print('before', df, weights)
		df = weighted_return(df, weights)
		print('after', df, weights)
		data_start = df.index.searchsorted(start)
		data_end = df.index.searchsorted(end)
		df = df.ix[data_start : data_end]
		df = df.round(2)
		df.drop(['Open', 'High', 'Low', 'Volume', 'Adj Close'],axis=1,inplace=True)
		frames.append(df)
	return frames

def add_columns(df):
	df['30-Day Return'] = df['Close']*100 / df['Close'].shift(22) - 100
	df['60-Day Return'] = df['Close']*100 / df['Close'].shift(44) - 100
	df['90-Day Return'] = df['Close']*100 / df['Close'].shift(66) - 100
	df['180-Day Return'] = df['Close']*100 / df['Close'].shift(132) - 100
	df['360-Day Return'] = df['Close']*100 / df['Close'].shift(264) - 100
	return df

def weighted_return(df, weights):
	three_sixty = 1 - sum(weights)
	if three_sixty < 0:
		three_sixty = 0
	df['Weighted Return'] = (
		df['30-Day Return']*weights[0] + df['60-Day Return']*weights[1] 
		+ df['90-Day Return']*weights[2] + df['180-Day Return']*weights[3] 
		+ df['360-Day Return']*three_sixty)
	return df

def float_option(wt):
	try:
		x = float(wt)
	except Exception as e:
		print(e)
		x = 0
	return x



