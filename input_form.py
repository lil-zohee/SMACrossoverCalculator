import json
import config
import numpy as np
import stock_math as sm
from bs4 import BeautifulSoup
from urllib.request import urlopen

class InputForm:
    def __init__(self, form):
        self.symbol = form.get('symbol-input').upper()
        self.interval = form.get('interval-input').strip()
        self.limit = int(form.get('limit-input'))
        self.multiple = {'1Min': 1, '5Min': 5, '15Min': 15, '1D': 1}[self.interval]

    def is_valid(self):
        if self.interval in ['1Min', '5Min', '15Min', '1D']:
            if 1 <= self.limit <= 1000:
                df = config.api.get_barset(self.symbol, self.interval, self.limit)[self.symbol].df
                if not df.empty:
                    self.series = df['close']
                    self.volume = df['volume']
                    self.dates = df.index
                    self.series.index = np.arange(0, self.series.shape[0])
                    return True
        return False

    def sma_windows(self):
        sma_short_window = self.series.shape[0] // 20
        sma_long_window = sma_short_window * 3
        if self.interval == '1D':
            sma_short_window = f'{sma_short_window} Day SMA'
            sma_long_window = f'{sma_long_window} Day SMA'
        else:
            sma_short_window = f'{sma_short_window} Min SMA'
            sma_long_window = f'{sma_long_window} Min SMA'
        return sma_short_window, sma_long_window

    def cross(self):
        sma_short, sma_long = sm.dual_sma(self.series)
        for i in range(self.series.shape[0] - 1, -1, -1):
            short_slope, short_int = sm.coef_of(i - 1, sma_short[i - 1], i, sma_short[i])
            long_slope, long_int = sm.coef_of(i - 1, sma_long[i - 1], i, sma_long[i])
            x_int, y_int = sm.intercept_of(short_slope, short_int, long_slope, long_int)
            if i - 1 <= x_int <= i:
                cross_point = self.dates[i - 1].to_pydatetime()
                cross_point = cross_point.strftime('%m/%d/%Y, %H:%M:%S')
                return cross_point, self.series.iloc[i - 1]

    def current_price(self):
        url = f'https://finance.yahoo.com/quote/{self.symbol}'
        html_content = urlopen(url).read()
        html_parser = BeautifulSoup(html_content, 'html.parser')
        price_html = html_parser.find('span', attrs={'data-reactid': '50'})
        try:
            return '$' + price_html.text
        except AttributeError:
            return 'ERROR'

    def price_change(self):
        cross_price = self.cross()[1]
        current_price = self.series.iloc[-1]
        change = current_price - cross_price
        change_percent = round((change / cross_price) * 100, 2)
        if change < 0:
            return f'${round(change, 2)} ({change_percent}%)', 'text-danger'
        return f'${round(change, 2)} ({change_percent}%)', 'text-success'

    def graph_data(self):
        X = list(self.series.index * self.multiple)
        sma_short, sma_long = sm.dual_sma(self.series)
        sma_short, sma_long = sma_short.round(2), sma_long.round(2)
        sma_short_window, sma_long_window = self.sma_windows()
        return json.dumps({
            'labels': X,
            'datasets': [
                {
                    'label': 'Closing Prices',
                    'fill': False,
                    'data': list(self.series),
                    'borderColor': 'rgba(0, 128, 255, 1)'
                },
                {
                    'label': sma_short_window,
                    'fill': False,
                    'data': list(sma_short),
                    'borderColor': 'rgba(255, 140, 0, 1)'
                },
                {
                    'label': sma_long_window,
                    'fill': False,
                    'data': list(sma_long),
                    'borderColor': 'rgba(0, 209, 0, 1)'
                }
            ]
        })

    def data(self):
        dual_sma_decision = sm.dual_sma(self.series, decision=True)
        xlabel = 'Days'
        if self.interval in ['1Min', '5Min', '15Min']:
            xlabel = 'Minutes'
        return (
            dual_sma_decision,
            self.cross(),
            self.current_price(),
            int(self.series.mean()),
            self.price_change(),
            xlabel,
            self.graph_data()
        )
