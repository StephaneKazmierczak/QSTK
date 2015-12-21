import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da
import datetime as dt
import matplotlib.pyplot as plt
# import pandas as pd


def main():

    ls_symbols = ["AAPL", "GLD", "GOOG", "$SPX", "XOM"]
    dt_start = dt.datetime(2006, 1, 1)
    dt_end = dt.datetime(2010, 12, 31)
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
    plt.clf()
    plt.plot(ldt_timestamps, na_price)
    plt.legend(ls_symbols)
    plt.ylabel('Adjusted Close')
    plt.xlabel('Date')
    plt.savefig('adjustedclose.pdf', format='pdf')

    # normalizing the plot
    na_normalized_price = na_price / na_price[0, :]

    plt.clf()
    plt.plot(ldt_timestamps, na_normalized_price)
    plt.legend(ls_symbols)
    plt.ylabel('Normalized Closed')
    plt.xlabel('Date')
    plt.savefig('normalizedclose.pdf', format='pdf')

    # daily return calculation inplace
    na_rets = na_normalized_price.copy()
    tsu.returnize0(na_rets)

    # dailyreturn plot 50 days XOM & &SPX
    plt.clf()
    plt.plot(ldt_timestamps[0:50], na_rets[0:50, 3])
    plt.plot(ldt_timestamps[0:50], na_rets[0:50, 4])
    plt.legend(ls_symbols[3:])
    plt.ylabel('Daily Returns')
    plt.xlabel('Date')
    plt.savefig('normalizeddailyreturn.pdf', format='pdf')

    # scatter plots
    plt.clf()
    plt.scatter(na_rets[:, 3], na_rets[:, 4], c='blue')
    plt.ylabel('XOM')
    plt.xlabel('$SPX')
    plt.savefig('scatterSPXvXOM.pdf', format='pdf')


# tsu.returnize0(na_rets)
# daily_cum_ret(t) = daily_cum_ret(t-1) * (1 + daily_ret(t))
