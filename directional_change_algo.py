import mplfinance as mpf
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.signal import argrelextrema
import seaborn as sns
import pandas_ta as ta
import math



def directional_change(close: np.array, high: np.array, low: np.array, atr: np.array, ret: float, window: int):

    while True:
        # adjusting prices and indeces based on window
        adj_idx = len(close) - window # Start point based on the dataframe

        adj_close = close[-window:]
        adj_high = high[-window:]
        adj_low = low[-window:]
        adj_atr = atr[-window-1:] # Its more accurate to incorporate the previous candle's ATR to understand the retracement of the currect candle


        up_zig = True # Assuming First candle is a Low/bottom
        tmp_max = adj_high[0] # Temporary top is the high of the fist candle
        tmp_min = adj_low[0]  # Temporary low is the low of the fist candle
        tmp_max_i = 0 # Index of temp high
        tmp_min_i = 0 # Index of temp low

        tops = []
        bottoms = []
        last_two_pivots = []

        for i in range(len(adj_close)):

            if up_zig:  #last extreme is a buttom
                if adj_high[i] > tmp_max: #new high, update
                    tmp_max = adj_high[i]
                    tmp_max_i = i

                elif adj_low[i] < tmp_max - (3 * adj_atr[i]):  # Price retraced by 3 times ATR. Top confirmed

                    if len(last_two_pivots) >= 2:
                        recent_move = abs(last_two_pivots[-1] - tmp_max)
                        ret_level = tmp_max - (recent_move * ret)
                        if adj_low[i] > ret_level:
                            continue  # Ignore this pivot

                    top = [tmp_max_i + adj_idx, tmp_max] # [index of top, price of top]
                    tops.append(top)
                    last_two_pivots.append(tmp_max)
                    if len(last_two_pivots) > 2: last_two_pivots.pop(0)


                    #setup for next bottom
                    up_zig = False
                    tmp_min = adj_low[i]
                    tmp_min_i = i


            else:  #last extreme is a top
                if adj_low[i] < tmp_min: # new low, update
                    tmp_min = adj_low[i]
                    tmp_min_i = i

                elif adj_high[i] > tmp_min + (3 * adj_atr[i]):  # Price retraced by by 3 times ATR. bottom confirmed, record it

                    if len(last_two_pivots) >= 2:
                        recent_move = abs(last_two_pivots[-1] - tmp_min)
                        ret_level = tmp_min + (recent_move * ret)
                        if adj_high[i] < ret_level:
                            continue  # Ignore this pivot

                    bottom = [tmp_min_i + adj_idx, tmp_min] # [index of bottom, price of bottom]
                    bottoms.append(bottom)
                    last_two_pivots.append(tmp_min)
                    if len(last_two_pivots) > 2: last_two_pivots.pop(0)

                    # Setup for next top
                    up_zig = True
                    tmp_max = adj_high[i]
                    tmp_max_i = i

        # Extract turning points indexes and prices
        pivots = tops + bottoms
        pivots.sort()
        pivots_indexes = [point[0] for point in pivots]
        pivots_indexes.append(len(adj_close) + adj_idx -1) # Appending the last close index
        pivots_prices = [point[1] for point in pivots]
        pivots_prices.append(adj_close[-1]) # Appending the last close price

        if len(pivots_indexes) < 8 and window + 100 <= len(close):
            window += 100
            continue
        else:
            break

    return pivots_indexes, pivots_prices