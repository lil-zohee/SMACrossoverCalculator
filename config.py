import alpaca_trade_api as tradeapi

api_key = '' # <-- Your Alpaca API Key Here
secret_key = '' # <-- Your Alpaca Secret Key Here
api = tradeapi.REST(api_key, secret_key, 'https://paper-api.alpaca.markets')
