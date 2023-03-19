import ccxt

class Bitstamp():
    def __init__(self, conf):
        self.exchange = ccxt.bitstamp({
            'apiKey': conf["api_key"],
            'secret': conf["api_secret"]
        })

    def get_transactions(self):
        raw_transactions = self.exchange.fetchMyTrades()

        transactions = {}

        for raw_transaction in raw_transactions:
            order = raw_transaction["order"]
            if order not in transactions.keys():
                transactions[order] = raw_transaction
            else:
                first_order_price = transactions[order]['price']
                first_order_amount = transactions[order]['amount']
                first_order_fee = transactions[order]['fee']['cost']

                second_order_price = raw_transaction['price']
                second_order_amount = raw_transaction['amount']
                second_order_fee = raw_transaction['fee']['cost']
            
                total_amount = first_order_amount + second_order_amount
                avg_price = (first_order_price * first_order_price + second_order_price * second_order_amount) / total_amount
                total_fee = first_order_fee + second_order_fee

                transactions[order]['price'] = avg_price
                transactions[order]['amount'] = total_amount
                transactions[order]['fee']['cost'] = total_fee

        print(transactions)
        return raw_transactions

    def sell(self, symbol, amount):
        try:
            response = self.exchange.create_market_sell_order(symbol, amount)
            return response
        except Exception as e:
            print('Failed to create sell order', type(e).__name__, str(e))
            return None
