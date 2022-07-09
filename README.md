# bitstamp-pnl-dashboard

This is Bitstamp PnL dashboard. Because Bitstamp has no shorting enabled, we are only showing long positions.
Top bar shows current prices of tickers that we find in non-hidden transactions.

## Info

**Hiding**
You are free to close position on your own and hide it manually once you close it. Because you may have old transactions that you already closed, there is Hide all button, to start blank.

**Selling**
Sell button exists, but is disabled for safety reasons. In order to sell you need to add capabilities to the api key, to be able to sell position and fix url in index.html from `<a href="#">` to `<a href="/hide?id={{ transaction['id'] }}">`

## Installation

```
pip install -r requirements.txt
export FLASK_APP=app
flask run
```