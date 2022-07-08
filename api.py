import ccxt

class Bitstamp():
    def __init__(self, conf):
        self.exchange = ccxt.bitstamp({
            'apiKey': conf["api_key"],
            'secret': conf["api_secret"]
        })

    def get_transactions(self):
        return self.exchange.fetchMyTrades()