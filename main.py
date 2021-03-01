from model.ticker_model import Ticker

ticker_list = ('aapl', 'zm')

if __name__ == '__main__':

    for ticker in ticker_list:
        ticker = Ticker(ticker)

        print(ticker.price_df)

        print(ticker.trend_25ma)