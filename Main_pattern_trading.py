# confirmation before starting the trade
# find a way to add to winning trades, we are getting out of profitable trades so fast
# Check directional change function and change variable names to something better
# Variables have significant effect on the restlt, we need to find a way to optimise them based on the market conditions
# Max Drawdown needs to get calculated + fluctuations
# find a way to evalute performance of each set of trades over your dataset
# Largest number of consecutive losses
# Average number of consecutive losses
# Average trading account % drawdown
# average holding Time




import pandas as pd
import pandas_ta as ta
import numpy as np
import matplotlib.pyplot as plt
from directional_change_algo import *
from harmonic_patterns import *
from visualizations import *
from walk_forward import *
from tqdm import tqdm
from tabulate import tabulate
import time
import seaborn as sns
import ta

df = pd.read_csv('data/btc-usdt-1m-OHLC-data-2018-09-08-19.56-utc-to-2022-09-07-20.18-utc.kaggle.csv')
df = df.drop(columns=['Unnamed: 0'])
df.columns = ['Date', 'open', 'high', 'low', 'close']
df["Date"] = pd.to_datetime(df["Date"])
df = df.set_index(df.Date)

#dropping the Date column
df = df[['open', 'high', 'low', 'close']]

# Identify consecutive duplicate rows across all columns
mask = ~(df == df.shift()).all(axis=1)

# Apply mask to keep only non-consecutive duplicates
df = df[mask]

df['atr'] = ta.volatility.AverageTrueRange(
    df.high,
    df.low,
    df.close,
    window=14,  #Last 14 candles
    fillna=None
).average_true_range()

df.ta.sma(length=1440, append=True)
df.ta.sma(length=60, append=True)


oprice = df['open'].copy()
hprice = df['high'].copy()
lprice = df['low'].copy()
cprice = df['close'].copy()
atr = df['atr'].copy()
sma_1d = df['SMA_1440'].copy()
sma_1h = df['SMA_60'].copy()


# ---0--- initials
wins = pats = longs = total_fee = 0
stoploss_changes = []
buynhold_value = []
pnl = np.array([])
balance = [10000]
ret = 0.3
dir_change_window = 300
harmonic_entry = True
random_entry = False
sma_entry = False
fees_enabled = True
pattern_err = 1/100
risk_threshold = 1/100
multiplier = 25
i = 1500
fee = 0.02 / 100 if fees_enabled else 0


pbar = tqdm(total=len(cprice)-i)

while i < len(cprice):

    # ---01--- Pivot Detector
    current_idx, current_pat = directional_change(cprice.values[:i],
                                                  hprice.values[:i],
                                                  lprice.values[:i],
                                                  atr.values[:i],
                                                  ret,
                                                  dir_change_window
                                                  )



    # ---02--- Entry Finder
    if harmonic_entry:
        patterns = [gartley, butterfly, bat, crab]
        for pattern in patterns:
            result = pattern(current_pat[-5:], pattern_err)
            if result is not None:
                sign, label = result
                break
        else:
            i += 1
            pbar.update()
            continue

    elif random_entry:
        label = 'random'
        if pats % 2 == 0:
            sign = 1
        else:
            sign = -1

    elif sma_entry:
        label = 'random'
        if cprice.values[current_idx[-1]] > sma_1d.values[current_idx[-1]]:
            sign = 1
        elif cprice.values[current_idx[-1]] < sma_1d.values[current_idx[-1]]:
            sign = -1

    pats += 1



    # ---03--- Trading
    trade_result, iteration, paid_fee = walk_forward(
        cprice.values[current_idx[-1]:],
        lprice.values[current_idx[-1]:],
        hprice.values[current_idx[-1]:],
        atr.values[current_idx[-1]:],
        sign,
        balance[-1],
        risk_threshold,
        multiplier,
        fee,
    )



    # ---04--- Calcualtions
    trade_result = trade_result - paid_fee

    if trade_result > 0: wins += 1
    if sign == 1: longs += 1

    total_fee += paid_fee

    winratio = round((wins / pats), 4) * 100

    # updating balance list
    balance.append(balance[-1] + trade_result)

    pnl = np.append(pnl, trade_result)
    cumpnl = pnl.cumsum()

    # buy and hold calculation
    buynhold_value.append((balance[0]/cprice.iloc[0]) * cprice.iloc[i])

    i += iteration
    pbar.update(iteration)
    stoploss_changes.append(iteration)


    # ---05--- Lets Visu visu
    # if i % 100 == 0:
    balance_chart(balance, buynhold_value)
        # pattern_chart(df, current_idx[:], current_pat[:], label, trade_result)
        # pnl_distribution_chart(pnl,winratio)
        # boxplot_chart(pnl)


    if balance[-1] <= 10:
        break

# ---06--- Getting Stats
print(f'\nNumber of trades: {pats}\n'
      f'Win ratio: %{round((wins/pats), 4)*100}\n'
      f'Profit factor: {round(np.mean(pnl[pnl > 0]) / abs(np.mean(pnl[pnl <= 0])), 2)}\n'
      f'Edge: {(wins/pats)*(np.mean(pnl[pnl > 0]))-(1-(wins/pats))*np.mean(pnl[pnl <= 0])}\n'
      f'Return on initial capital: % {round((balance[-1]-balance[0])*100/balance[0],2)}\n'
      f'Average PNL: {np.mean(pnl)} $\n'
      f'Median of PNL: {np.median(pnl)} $\n'
      f'Total net profit/loss: {cumpnl[-1]} $\n'
      f'\n'
      f'Buy and Hold profit/loss: %{((buynhold_value[-1]-balance[0])/balance[0])*100}\n'
      f'\n'
      f'Number of win trades: {wins}\n'
      f'Mean of gains: {np.mean(pnl[pnl > 0])} $\n'
      f'Median of gains: {np.median(pnl[pnl > 0])} $\n'
      f'Maximum gain: {max(pnl)} $\n'
      f'\n'
      f'Number of loss trades: {pats - wins}\n'
      f'Mean of losses: {np.mean(pnl[pnl <= 0])} $\n'
      f'Median of losses: {np.median(pnl[pnl <= 0])} $\n'
      f'Maximum loss: {min(pnl)} $\n'
      f'\n'
      f'Number of Short Trades: {pats-longs}\n'
      f'Number of Long Trades: {longs}\n'
      f'\n'
      f'average number of time stoploss moved within trades: {sum(stoploss_changes)/pats}\n'
      f'\n'
      f'Fee paid: {total_fee}\n'
      f'\n'
      f'--- Variable values ---\n'
      f'ret: {ret}\n'
      f'Directional Change Window: {dir_change_window}\n'
      f'Harmonic Entry: {harmonic_entry}\n'
      f'Random Entry: {random_entry}\n'
      f'SMA Entry: {sma_entry}\n'
      f'Pattern Error Allowed: {pattern_err}\n'
      f'Risk Threshold: {risk_threshold}\n'
      f'Multiplier: {multiplier}\n'
      f'Fees Enabled: {fees_enabled}\n'
      )


plt.ioff()
plt.show()
