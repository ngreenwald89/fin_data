import datetime
import timeit
import io
import pandas as pd
import pandas_datareader.data as web
from parameters import parameters

def excel_test(parameters):
	dfs = make_df(parameters=parameters)
	output = io.BytesIO()
	writer = pd.ExcelWriter(output, engine='xlsxwriter')
	for df in dfs:
		df_symbol = df['Symbol'].values[0]
		df.to_excel(writer,df_symbol)
	writer.close()
	output.seek(0)
	r = output.read()
	return r

def make_df(parameters):
	# prepare parameters
	start, end = make_date_objects(parameters['start_date'], parameters['end_date'])
	# weights = [float(parameters['thirty_day_weight']), float(parameters['sixty_day_weight']), float(parameters['ninety_day_weight']), float(parameters['one_eighty_day_weight'])]
	weights = [
		float_option(parameters['thirty_day_weight']), float_option(parameters['sixty_day_weight']), 
		float_option(parameters['ninety_day_weight']), float_option(parameters['one_eighty_day_weight'])
			]
	symbols = parameters['symbols']
	# make the API calls and build the dataframe
	frames = separate_frames(symbols=symbols, start=start, end=end, weights=weights)
	return frames

def make_date_objects(*dates):
	date_objects = []
	for date in dates:
		print('date before split', date)
		date = [int(string) for string in date.split('-')]
		print('date after split', date)
		obj=datetime.date(date[0], date[1], date[2])
		date_objects.append(obj)
	return date_objects

def separate_frames(symbols, start, end, weights):
	real_start = start - datetime.timedelta(days=400)
	frames = []
	for symbol in symbols:
		df = web.DataReader(symbol, 'yahoo', real_start, end)
		df = add_columns(df)
		df['Symbol'] = symbol
		df = calc_index(df, weights)
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

def calc_index(df, weights):
	three_sixty = 1 - sum(weights)
	if three_sixty < 0:
		three_sixty = 0
	df['Index Calc'] = df['30-Day Return']*weights[0] + df['60-Day Return']*weights[1] + df['90-Day Return']*weights[2] + df['180-Day Return']*weights[3] + df['360-Day Return']*three_sixty
	return df

def make_df(parameters):
	# prepare parameters
	start, end = make_date_objects(parameters['start_date'], parameters['end_date'])
	# weights = [float(parameters['thirty_day_weight']), float(parameters['sixty_day_weight']), float(parameters['ninety_day_weight']), float(parameters['one_eighty_day_weight'])]
	weights = managing_weights(parameters)
	"""
	weights = [
		float_option(parameters['thirty_day_weight']), 
		float_option(parameters['sixty_day_weight']), 
		float_option(parameters['ninety_day_weight']), 
		float_option(parameters['one_eighty_day_weight'])
	]
	"""
	symbols = parameters['symbols']
	# make the API calls and build the dataframe
	final_df = do_symbols(symbols=symbols, start=start, end=end, weights=weights)
	return final_df

def float_option(wt):
	try:
		x = float(wt)

	except Error as e:
		print(e)
		x = 0
	return x

def managing_weights(parameters):
	remainder = 1
	weights = []
	for wt in [parameters['thirty_day_weight'], parameters['sixty_day_weight'], parameters['ninety_day_weight'], parameters['one_eighty_day_weight']]:
		print(wt)
		wt = float_option(wt)
		if wt >= 1:
			wt = 0
		elif remainder - wt >= 0:
			weights.append(wt)
			remainder -= wt
		# if wt > remainder, give wt zero
		else:
			weights.append(0)
	# 360 day value gets remainder
	if remainder >= 0:
		weights.append(remainder)
	return weights


def write_to_csv(df, parameters):
	writer = pd.ExcelWriter(parameters['filename']+".xlsx")
	tickers = df['Symbol'].unique()
	ticker_dfs = []
	for ticker in tickers:
		ticker_df = df[df['Symbol']==ticker]
		slimmed_down = ticker_df.loc[parameters['start_date']:parameters['end_date']]
		slimmed_down.to_excel(writer, ticker)
	writer.save()
	return writer

def run_get_data(parameters):
	df = make_df(parameters=parameters)
	# df.to_csv(parameters['filename'])
	write_to_csv(df=df, parameters=parameters)

def some_data(parameters):
	df = make_df(parameters=parameters)
	col_names = list(df.columns.values)
	top_row = df.iloc[0]
	dic = dict(zip(col_names, top_row))
	# write_to_csv(df, parameters)
	csv = df.to_csv()
	return csv


