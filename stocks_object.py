import yfinance as yf


class StockObject:
    def __init__(self, ticker):
        self.full_name = None
        self.last_close = None
        self.stock = yf.Ticker(ticker)
        self.ignore = False
        self.load_values()

    def load_values(self):
        self.full_name = self.stock.info['longName']
        self.last_close = self.stock.history(period="1d")["Close"][0]

    def get_current_price(self):
        return self.stock.info["regularMarketPrice"]

    def get_current_percentage(self):
        return self.get_current_price() / self.last_close

    def new_day(self):
        self.last_close = self.stock.history(period="1d")["Close"][0]
        self.ignore = False

    def ignore(self):
        self.ignore = True

    def get_ignore(self):
        return self.ignore
