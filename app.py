
import os
import json
import yaml
import copy
import pickle
import requests
from api import Bitstamp
from flask import Flask, render_template, request, redirect

with open("config.yaml",) as f:
    conf = yaml.load(f, Loader=yaml.FullLoader)
api = Bitstamp(conf)
app = Flask(__name__)

@app.route("/")
def index():
    tickers, transactions = enrich_data(remove_blacklisted(api.get_transactions()))
    return render_template("index.html", transactions=transactions[::-1], tickers=tickers)

def remove_blacklisted(transactions):
    closed = get_closed()
    active_transactions = copy.copy(transactions)
    for transaction in transactions:
        if str(transaction['id']) in closed or transaction["side"] == "sell":
            active_transactions.remove(transaction)
    return active_transactions

def get_closed():
    txs = []
    if os.path.exists("closed.pkl"):
        with open("closed.pkl", "rb") as f:
            txs = pickle.load(f)
    print("Closed txs:", txs)
    return txs

def enrich_data(transactions):
    tickers = []
    for transaction in transactions:
        if transaction["symbol"] not in tickers:
            tickers.append(transaction["symbol"])

    ticker_data = {}
    for ticker in tickers:
        url_ticker = ticker.replace("/", "").lower()
        url = "https://www.bitstamp.net/api/v2/ohlc/{}/?step=60&limit=1".format(url_ticker)
        response = requests.get(url)
        price_data = json.loads(response.text)
        ticker_data[ticker] = price_data["data"]["ohlc"][0]["close"]

    for index, transaction in enumerate(transactions):
        transactions[index]["current_price"] = float(ticker_data[transaction["symbol"]])

    return ticker_data, transactions

@app.route("/close", methods=['GET'])
def close():
    args = request.args
    txid = args.get("id")

    txs = []
    if os.path.exists("closed.pkl"):
        with open("closed.pkl", "rb") as f:
            txs = pickle.load(f)

    if txid not in txs:
        txs.append(txid)

    with open("closed.pkl", "wb") as f:
        pickle.dump(txs, f)
    return redirect('/')

@app.route("/transactions")
def transactions():
    return json.dumps(api.get_transactions())