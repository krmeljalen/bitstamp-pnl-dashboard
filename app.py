
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
    hidden = get_hidden()
    active_transactions = copy.copy(transactions)
    for transaction in transactions:
        if str(transaction['id']) in hidden or transaction["side"] == "sell":
            active_transactions.remove(transaction)
    return active_transactions

def get_hidden():
    txs = []
    if os.path.exists("hidden.pkl"):
        with open("hidden.pkl", "rb") as f:
            txs = pickle.load(f)
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

@app.route("/hide", methods=['GET'])
def hide():
    args = request.args
    txid = args.get("id")

    txs = []
    if os.path.exists("hidden.pkl"):
        with open("hidden.pkl", "rb") as f:
            txs = pickle.load(f)

    if txid not in txs:
        txs.append(txid)

    with open("hidden.pkl", "wb") as f:
        pickle.dump(txs, f)
    return redirect('/')

@app.route("/hideall")
def hideall():
    txs = []
    if os.path.exists("hidden.pkl"):
        with open("hidden.pkl", "rb") as f:
            txs = pickle.load(f)

    for transaction in api.get_transactions():
        if transaction["id"] not in txs:
            txs.append(transaction["id"])

    with open("hidden.pkl", "wb") as f:
        pickle.dump(txs, f)
    return redirect('/')

@app.route("/transactions")
def transactions():
    return json.dumps(api.get_transactions())