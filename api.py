import ccxt

class Bitstamp():
    def __init__(self, conf):
        self.exchange = ccxt.bitstamp({
            'apiKey': conf["api_key"],
            'secret': conf["api_secret"]
        })

    def get_transactions(self):
        return self.exchange.fetchMyTrades()

    def sell(self, symbol, amount):
        try:
            response = self.exchange.create_market_sell_order(symbol, amount)
            return response
        except Exception as e:
            print('Failed to create sell order', type(e).__name__, str(e))
            return None
