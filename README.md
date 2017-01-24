https://stockreturns123.herokuapp.com

# fin_data
Download stock data, get approximate 30, 60, 90, 180, and 360 day returns, plus a field to weight those returns.
N day return for day X: (X*100)/N-100.

So if stock price was 50 on 12/31/16, and 44 on 12/01/16, then 30 day return = (50*100)/44-100 = 13.63%.

Weighted_return = wt30*30day + wt60*60day + wt90*90day + wt180*180day + wt360*360day, 
where wt360 is the remainder of 1-sum(other weights). Each weight should be 0 <= wt <= 1

To run on localhost:

1. Download repo: 

$ git clone https://github.com/ngreenwald89/fin_data.git

$ cd /path/to/fin_data

2. When cloning for the first time, make virtual environment. if you don't have virtualenv, install with pip: pip install virtualenv. skip to activating environment in the future.

$ virtualenv `<env directory name>`

$ source `<env directory name>`/bin/activate #activate environment.

$ pip install -r requirements.txt #installs the requirements

$ python fin_data.py #app now running on 0.0.0.0:5000. can also run with python3

to deactivate environment:

$ deactivate
