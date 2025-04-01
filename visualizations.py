import mplfinance as mpf
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import math


def balance_chart(balance, buynhold_value):

    plt.clf()
    plt.plot(balance, label='Balance', c='b')
    plt.plot(buynhold_value, label='Buy N Hold value', c='r')
    plt.xlabel('Trades')
    plt.ylabel('Balance')
    plt.title('Balance over time')
    plt.legend()
    plt.ion()
    plt.pause(math.ulp(1.0))


def pnl_distribution_chart(pnl, winratio):

    plt.clf()
    sns.histplot(pnl, bins=50, color='black', kde=True)
    plt.xlabel('PNL')
    plt.ylabel('Freq')
    plt.title(str(winratio))
    plt.ion()
    plt.pause(math.ulp(1.0))


def boxplot_chart(pnl):
    plt.clf()
    sns.boxplot(pnl, flierprops={"marker": "_"},)
    plt.title('PNL Boxplot')
    plt.ion()
    plt.pause(math.ulp(1.0))



def pattern_chart(df, current_idx, current_pat, label, pips):

    after_pattern = 0
    pattern_dates = df.index[current_idx[0]:current_idx[-1]+1 + after_pattern]

    data_slice = current_idx[-1] - current_idx[0] +1 + after_pattern

    # Create an array for the pattern data with the same length as the data slice
    pattern_data = np.full(data_slice, np.nan)

    # Adjust the indices to be relative to the data slice
    relative_indices = [i - current_idx[0] for i in current_idx]

    # Fill the pattern data
    pattern_data[relative_indices] = current_pat

    df1 = pd.DataFrame(data=pattern_data, index=pattern_dates, columns=['cp'])
    df1 = df1.interpolate(limit_area='inside')

    legend = str(round(pips,2)) + ' ' + '$'

    # plt.ion()
    # plt.clf()
    mpf.plot(df.iloc[current_idx[0]:current_idx[-1]+1 + after_pattern],
             type='candle',
             style='starsandstripes',
             title=label,
             ylabel='Price',
             xlim=(0, current_idx[-1] - current_idx[0]+1 + after_pattern),
             figratio=(10, 6),
             addplot=mpf.make_addplot(df1,
                                        type='line',
                                        color='black',
                                        width=2,
                                        panel=0,
                                        secondary_y=False,
                                        label=legend),
             )
    # plt.pause(0.5)