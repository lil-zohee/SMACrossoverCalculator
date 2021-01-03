def dual_sma(series, decision=False):
    sma_rate = series.shape[0] // 20
    sma_short = series.rolling(sma_rate).mean()
    sma_long = series.rolling(sma_rate * 3).mean()
    if decision:
        if sma_short.iloc[-1] >= sma_long.iloc[-1]:
            return 'Bullish', 'text-success'
        return 'Bearish', 'text-danger'
    return sma_short, sma_long

def coef_of(x1, y1, x2, y2):
    rise = y2 - y1
    run = x2 - x1
    slope = rise / run
    y_int = y1 - (slope * x1)
    return slope, y_int

def intercept_of(slope1, y_int1, slope2, y_int2):
    slope = slope1 - slope2
    y_int = y_int2 - y_int1
    x = y_int / slope
    y = (slope1 * x) + y_int1
    return x, y
