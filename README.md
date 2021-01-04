# SMA Crossover Calculator
Try out the web application here --> http://smacrosscalc.pythonanywhere.com/
## Prerequisites
1. Have `Python3` and `pip` installed on PC.  (Install from https://python.org)
2. Have `git` installed.  (Install from https://git-scm.com/downloads)
3. Have an Alpaca Markets account.  (Create one at https://alpaca.markets/)

## Setup
1. `git clone` the repository
```sh
git clone https://github.com/lil-zohee/SMACrossoverCalculator.git
```
2. Move in the new directory
```sh
cd SMACrossoverCalculator/
```
3. Install all necessary modules
```sh
pip3 install -r requirements.txt
```
4. Edit `config.py` and provide your Alpaca Markets API and Secret Key.  (To find it, go to your [paper account dashboard](https://app.alpaca.markets/paper/dashboard/overview))
```python
import alpaca_trade_api as tradeapi

api_key = '' # <-- Your Alpaca API Key Here
secret_key = '' # <-- Your Alpaca Secret Key Here
api = tradeapi.REST(api_key, secret_key, 'https://paper-api.alpaca.markets')
```
5. Finally, run the web application
```sh
python3 main.py
```
