
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