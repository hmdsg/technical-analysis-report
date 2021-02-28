from model.ticker_model import Ticker

if __name__ == '__main__':


    ticker = Ticker("aapl")

    print(ticker.price_df)

    print(ticker.trend_25ma)

    print(ticker.domination_rate_25ma)