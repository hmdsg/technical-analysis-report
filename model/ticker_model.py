from dataclasses import dataclass
import pandas as pd

dfType = pd.core.frame.DataFrame


@dataclass
class Ticker:
    name: str
    price_df: dfType = None

    def trend_direction(self) -> str:
        """
   　　　直近のMA_25の向きを返す。
        前々日の25_MAより大きければup,小さければdownを返す。
        :return:
        """
        if self.price_df.iloc[-1]['MA_25'] - self.price_df.iloc[-2]['MA_25'] > 0:
            return 'up'
        elif self.price_df.iloc[-1]['MA_25'] - self.price_df.iloc[-2]['MA_25'] < 0:
            return 'down'
        else:
            return 'keep'

    def get_trend(self):
        """
        前日を除く過去3日間の終値を参考にトレンドを返す
        :return:
        """
        last_trend_list = []

        assert self.price_df is not


        # 日毎の判定
        for n in range(-4, -1):
            if self.price_df.iloc[n]['Close'] - self.price_df.iloc[n]['MA_25'] > 0:
                last_trend_list.append(1)
            elif self.price_df.iloc[n]['Close'] - self.price_df.iloc[n]['MA_25'] < 0:
                last_trend_list.append(-1)
            else:
                last_trend_list.append(0)

        # 全通りの判定
        if last_trend_list.index(1) == 3:
            return 'over'
        elif last_trend_list.index(-1) == 3:
            return 'under'
        else:
            return 'cross'
