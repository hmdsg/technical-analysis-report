import pandas as pd

STOCK_CODE_PATH = "./data/stock_code_jpn.csv"


def read_stock_stock_jpn(code: str) -> str:
    """
    銘柄コードから銘柄名を返す
    :param code: 銘柄コード
    :return: 銘柄名
    """
    # print (f"code is {code}")
    csv_input = pd.read_csv(filepath_or_buffer=STOCK_CODE_PATH, sep=",")
    stock_name = csv_input.query(f'コード ==  {code}')["銘柄名"].values[0]

    # print (f"return is {stock_name}")
    return stock_name
