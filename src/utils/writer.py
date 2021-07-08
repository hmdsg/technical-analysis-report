import mplfinance as mpf
import pandas as pd

dfType = pd.core.frame.DataFrame


def write(df: dfType, path: str, title=None):
    mpf.plot(df, savefig=path, title=title, type='candle', mav=(5, 25, 75), volume=True, datetime_format='%d/%m/%Y')
