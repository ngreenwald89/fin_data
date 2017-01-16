# fin_data
Download stock data, get approximate 30, 60, 90, 180, and 360 day returns, plus a field to weight those returns.
N day return for day X: (X*100)/N-100.

So if stock price was 50 on 12/31/16, and 44 on 12/01/16, then 30 day return = (50*100)/44-100 = 13.63%.

Weighted_return = wt30*30day + wt60*60day + wt90*90day + wt180*180day + wt360*360day, where wt360 is the remainder of 1-sum(other weights). Each weight should be 0 <= wt <= 1

