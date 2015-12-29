from __future__ import division
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da
import datetime as dt
# import matplotlib.pyplot as plt
# import pandas as pd
import numpy as np
import sys

# TODO: add command line parameters
# TODO: improve for loop of optimizer
# TODO: find another optimizer solution based
#       on stock comparaison (scater plot/sharp ratio plot)


def simulate(dt_start, dt_end, ls_symbols, ls_equities):

    # Simulate

    # retrive date
    dt_timeofday = dt.timedelta(hours=16)
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)

    c_dataobj = da.DataAccess('Yahoo')
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    ldf_data = c_dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))

    # Filling the data for NAN
    for s_key in ls_keys:
        d_data[s_key] = d_data[s_key].fillna(method='ffill')
        d_data[s_key] = d_data[s_key].fillna(method='bfill')
        d_data[s_key] = d_data[s_key].fillna(1.0)

    na_price = d_data['close'].values

    # normalizing the price of the portfolio
    na_normalized_price = na_price / na_price[0, :]

    # calculate portfolio daily value
    na_portfolio_price = na_normalized_price * np.array(ls_equities)

    # sum up the matrix of each equities to single col matrix
    na_sum = np.sum(na_portfolio_price, axis=1)

    return na_sum


def optimizer(dt_start, dt_end, ls_symbols):

    ls_equities = [0, 0, 0, 0]
    d_max_sharp_ratio = 0
    b_init_ratio = False

    # compute for each possible combinatoir wich sum 1 the best
    # equities composition based on highest sharpe ratio

    for i in range(0, 11):
        for j in range(0, 11):
            for k in range(0, 11):
                for l in range(0, 11):
                    if ((i + j + k + l) == 10):
                        na_sum = simulate(dt_start, dt_end, ls_symbols,
                                          [i/10, j/10, k/10, l/10])
                        na_rets = na_sum.copy()
                        tsu.returnize0(na_rets)

                        d_std = np.std(na_rets)
                        d_mean = np.mean(na_rets)
                        d_sharp_ratio = np.sqrt(252) * d_mean / d_std

                        if not(b_init_ratio):
                            d_max_sharp_ratio = d_sharp_ratio
                            ls_equities = [i/10, j/10, k/10, l/10]
                            b_init_ratio = True
                        elif (d_max_sharp_ratio < d_sharp_ratio):
                            d_max_sharp_ratio = d_sharp_ratio
                            ls_equities = [i/10, j/10, k/10, l/10]

    return ls_equities


def main(argv=None):

    dt_start = dt.datetime(2010, 1, 1)
    dt_end = dt.datetime(2010, 12, 31)
    ls_symbols = ["C", "GS", "IBM", "HNZ"]

    ls_equities = optimizer(dt_start, dt_end, ls_symbols)
    # ls_equities = [0.4, 0.4, 0.0, 0.2]
    na_sum = simulate(dt_start, dt_end, ls_symbols, ls_equities)

    na_rets = na_sum.copy()
    tsu.returnize0(na_rets)

    d_std = np.std(na_rets)
    d_mean = np.mean(na_rets)
    d_sharp_ratio = np.sqrt(252) * d_mean / d_std
    d_cum_sum = (na_sum[-1]-na_sum[0]) / na_sum[0]

    print "Start Date:", dt_start
    print "End Date:", dt_end
    print "Symbols", ls_symbols
    print "Optimal Allocations:", ls_equities
    print "Sharpe Ratio:", d_sharp_ratio
    print "Volatility (stdev of daily returns):", d_std
    print "Average Daily Return:", d_mean
    print "Cumulative Return:", (d_cum_sum+1)


if __name__ == "__main__":
    sys.exit(main())
