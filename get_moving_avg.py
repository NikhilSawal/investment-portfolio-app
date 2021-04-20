import pandas as pd

# Get simple moving average (SMA)
def sma(data, colName, period):
    temp = []
    for i in range(period, len(data[colName])):
        sma = round(sum(data[colName][i-period:i])/period,2)
        temp.append(sma)

    return [0 if i < period else temp[i-period] for i in range(len(data[colName]))]

# Get exponential moving average (EMA)
def ema(data, colName, period):

    alpha = 2/(period+1)
    sma_1 = sma(data, colName, period)
    temp = []

    for i in range(period, len(data[colName])):
        ema = (sum(data[colName][i:i+1])*alpha) + ((1-alpha)*sma_1[i-1])
        temp.append(ema)

    return [0 if i < period else temp[i-period] for i in range(len(data[colName]))]

# Get weighted moving average (WMA)
def wma(data, colName, period):

    denom = (period*(period+1))/2
    temp = []

    for i in range(period, len(data[colName])):

        time_window = [i for i in data[colName][i-period:i]]
        weighted = []

        for j in range(len(time_window)):

            weighted.append(time_window[j] * (j+1))

        weighted_sum = round(sum(weighted)/denom, 2)
        temp.append(weighted_sum)

    return [0 if i < period else temp[i-period] for i in range(len(data[colName]))]
