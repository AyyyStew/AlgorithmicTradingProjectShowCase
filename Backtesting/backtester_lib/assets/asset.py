# Asset class to store accounting information
class Asset:
    def __init__(self, starting_balance=1000, qty=0, buy_fee=0.005, sell_fee=0.005):
        self.balance = starting_balance
        self.qty = qty
        self.buy_fee = buy_fee
        self.sell_fee = sell_fee
        self.intial_args = {
            "starting_balance": starting_balance,
            "qty": qty,
        }

    def buy(self, price, percent_of_balance_to_buy=1):
        balance_to_buy = self.balance * percent_of_balance_to_buy
        qty_to_buy = balance_to_buy / (price * (1 + self.buy_fee))

        self.qty = self.qty + qty_to_buy
        self.balance = self.balance - balance_to_buy
        return self.balance

    def sell(self, price, percent_of_holding_to_sell=1):
        qty_to_sell = percent_of_holding_to_sell * self.qty
        gain = qty_to_sell * price * (1 - self.sell_fee)

        self.qty = self.qty - qty_to_sell
        self.balance = self.balance + gain
        return self.balance

    def get_holding_value(self, price):
        return self.balance + self.qty * price

    def reinitialize(self):
        self.balance = self.intial_args["starting_balance"]
        self.qty = self.intial_args["qty"]
