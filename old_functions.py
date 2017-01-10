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