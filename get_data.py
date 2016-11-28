import datetime
import timeit
import pandas as pd
import pandas_datareader.data as web
from parameters import parameters


def make_date_objects(*dates):
	date_objects = []
	for date in dates:
		print('date before split', date)
		date = [int(string) for string in date.split('-')]
		print('date after split', date)
		obj=datetime.date(date[0], date[1], date[2])
		date_objects.append(obj)
	return date_objects

def do_symbols(symbols, start, end, weights):
	frames = []
	real_start = start - datetime.timedelta(days=400)
	for symbol in symbols:
		df = web.DataReader(symbol, 'yahoo', real_start, end)
		df = add_columns(df)
		df['Symbol'] = symbol
		frames.append(df)
	group_df = pd.concat(frames)
	# below operations don't need to be done separately on each symbol
	group_df = calc_index(group_df, weights)
	group_df = group_df.round(2)
	group_df.drop(['Open', 'High', 'Low', 'Volume', 'Adj Close'],axis=1,inplace=True)
	return group_df

def add_columns(df):
	df['30-Day Return'] = df['Close']*100 / df['Close'].shift(22) - 100
	df['60-Day Return'] = df['Close']*100 / df['Close'].shift(44) - 100
	df['90-Day Return'] = df['Close']*100 / df['Close'].shift(66) - 100
	df['180-Day Return'] = df['Close']*100 / df['Close'].shift(132) - 100
	df['360-Day Return'] = df['Close']*100 / df['Close'].shift(264) - 100
	return df

def calc_index(df, weights):
	df['Index Calc'] = df['30-Day Return']*weights[0] + df['60-Day Return']*weights[1] + df['90-Day Return']*weights[2] + df['180-Day Return']*weights[3]
	return df

def make_df(parameters):
	# prepare parameters
	start, end = make_date_objects(parameters['start_date'], parameters['end_date'])
	weights = [float(parameters['thirty_day_weight']), float(parameters['sixty_day_weight']), float(parameters['ninety_day_weight']), float(parameters['one_eighty_day_weight'])]
	symbols = parameters['symbols']
	# make the API calls and build the dataframe
	final_df = do_symbols(symbols=symbols, start=start, end=end, weights=weights)
	return final_df

def write_to_csv(df, parameters):
	df.loc[parameters['start_date']:parameters['end_date']].to_csv(parameters['filename'])

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

# NOT USING FUNCTIONS BELOW AT THE MOMENT
def add_dates(df):
	df['30-day date'] = df.index.shift(-22, freq='B')
	df['60-day date'] = df.index.shift(-44, freq='B')
	df['90-day date'] = df.index.shift(-66, freq='B')
	df['180-day date'] = df.index.shift(-132, freq='B')
	df['360-day date'] = df.index.shift(-264, freq='B')
	return df

def wrapper(func, *args, **kwargs):
	def wrapped():
		return func(*args, **kwargs)
	return wrapped
