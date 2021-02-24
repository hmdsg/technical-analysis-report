from model.ticker_model import Ticker
from service import price_service as ps

if __name__ == '__main__':
    ticker = Ticker("zm")
    ticker.price_df = ps.get_price(ticker.name, '01/01/2020')

    print(ticker.price_df)
    ticker.price_df['MA_25']=ticker.price_df['Close'].rolling(25).mean().round(2)

    print (ticker.price_df)

    print(ticker.get_trend())