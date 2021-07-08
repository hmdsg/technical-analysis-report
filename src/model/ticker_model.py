from dataclasses import dataclass
from service import price_service as ps
from utils import stock
import pandas as pd
import math

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

dfType = pd.core.frame.DataFrame


@dataclass
class Ticker:
    code: str
    country: str
    price_df: dfType = None
    name: str = ""
    trend_25ma = 0
    trend_direction_25ma = 0
    last_line = 0
    last_position_25ma = 0
    deviation_rate_25ma = 0.0
    domination_rate_25ma = 0.0
    period_list_25ma = []

    def __post_init__(self):

        self.name = self._get_name()
        self.price_df = ps.get_price(self.code, self.country)
        self._insert_ma(25)
        self._insert_ma_vs_Close(25)
        self._insert_ma_domination_rate(25)
        self.trend_direction_25ma = self._get_trend_direction(25)
        self.deviation_rate_25ma = self._check_deviation_rate(25)
        self.period_list_25ma = [period for period in self._get_over_under_period(25)]
        print(self.period_list_25ma)


    def _get_name(self):
        """
        名前を取得する。
        米国株ではcodeが名前となる。
        :return: name
        """

        if self.country == "japan":
            return stock.read_stock_stock_jpn(self.code)
        else:
            return self.code

    def _insert_ma(self, ma_days: int):
        """
        dfに移動平均値を挿入する
        :param ma_days: 移動平均の日数
        :return:
        """
        assert self.price_df is not None
        ma_name = 'MA_' + str(ma_days)

        self.price_df[ma_name] = self.price_df['Close'].rolling(ma_days).mean().round(2)

    def _insert_ma_vs_Close(self, ma_days: int):
        """
        dfに終値と指定のmaの差を挿入する。
        値が正の場合は終値が移動平均値より高い。
        :param ma_days: 移動平均の日数
        """
        ma_name = 'MA_' + str(ma_days)
        assert self.price_df is not None

        self.price_df[f"{ma_name}_vs_Close"] = self.price_df['Close'] - self.price_df[ma_name]

    def _get_over_under_period(self, ma_days: int) -> int:
        ma_name = 'MA_' + str(ma_days)
        assert self.price_df is not None

        position = 1 if self.price_df.iloc[-1][f"{ma_name}_vs_Close"] > 0 else -1

        for index, diff in (enumerate(reversed(self.price_df[f"{ma_name}_vs_Close"]))):
            # 下のまま
            if diff < 0 and position == -1:
                position = -1
            # 上から下
            elif diff < 0 and position == 1:
                position = -1
                yield index + 1
            # 上のまま
            elif diff >= 0 and position == 1:
                position = 1
            # 下から上
            elif diff >= 0 and position == -1:
                position = 1
                yield index + 1
            elif math.isnan(diff):
                break
            else:
                print("unknown _get_over_under_period", index, diff, position)
                break


    def is_over_ma(self, ma_days: int, ref_day: int) -> bool:
        """
        ref_dayの終値がma_daysを超えているか判定する
        :param ma_days:
        :return: bool
        """
        ma_name = 'MA_' + str(ma_days)
        assert self.price_df is not None

        ref_day = ref_day * -1
        if self.price_df.iloc[ref_day][f"{ma_name}_vs_Close"] > 0:
            return True
        else:
            return False

    def _get_trend_direction(self, ma_days: int) -> int:
        """
   　　　指定の移動平均の方向を返す。
        前日の移動平均値が前々日の移動平均値より大きければ1,小さければ-1を返す。
        """
        ma_name = 'MA_' + str(ma_days)

        if self.price_df.iloc[-1][ma_name] - self.price_df.iloc[-2][ma_name] > 0:
            return 1
        elif self.price_df.iloc[-1][ma_name] - self.price_df.iloc[-2][ma_name] < 0:
            return -1
        else:
            return 0

    def get_trend(self, ref_days, ma_days: int) -> int:
        """
        指定日の終値を参考にトレンドを返す
        """
        ma_name = 'MA_' + str(ma_days)

        assert self.price_df is not None

        # 日毎の判定

        if self.price_df.iloc[ref_days]['Close'] - self.price_df.iloc[ref_days][ma_name] > 0:
            return 1
        elif self.price_df.iloc[ref_days]['Close'] - self.price_df.iloc[ref_days][ma_name] < 0:
            return -1
        else:
            return 0

    def _check_deviation_rate(self, ma_days: int) -> float:
        """
        前日の終値と移動平均値の乖離率を百分率で返す。
        """

        ma_name = 'MA_' + str(ma_days)

        return round(
            100 * (self.price_df.iloc[-1]['Close'] - self.price_df.iloc[-1][ma_name]) / self.price_df.iloc[-1]['Close'],
            1)

    def _insert_ma_domination_rate(self, ma_days: int):
        """
        ロウソク胴体の移動平均値からの剥離率


        """

        ma_name = 'MA_' + str(ma_days)
        column = ma_name + "_domination_rate"

        # 始値と終値が移動平均線を超えない時(胴体が移動平均線の下)
        self.price_df.loc[(self.price_df['Open'] <= self.price_df[ma_name]) & \
                          (self.price_df['Close'] <= self.price_df[ma_name]), column] \
            = -100

        # 始値と終値が移動平均線を超えている時(胴体が移動平均線の上)
        self.price_df.loc[(self.price_df['Open'] >= self.price_df[ma_name]) & \
                          (self.price_df['Close'] >= self.price_df[ma_name]), column] \
            = 100

        # 陰線で移動平均線をクロスしている時(胴体が移動平均線とクロス)
        self.price_df.loc[(self.price_df['Close'] < self.price_df[ma_name]) & \
                          (self.price_df['Open'] >= self.price_df[ma_name]), column] \
            = -100 * (self.price_df['Open'] - self.price_df[ma_name]) / \
              (self.price_df['Open'] - self.price_df['Close'])

        # 陽線で移動平均線をクロスしている時(胴体が移動平均線とクロス)
        self.price_df.loc[(self.price_df['Close'] > self.price_df[ma_name]) & \
                          (self.price_df['Open'] <= self.price_df[ma_name]), column] \
            = 100 * (self.price_df['Close'] - self.price_df[ma_name]) / \
              (self.price_df['Close'] - self.price_df['Open'])

    def is_positive_line(self, ref_day: int) -> bool:
        """
        相対的な指定日が陽線か陰線かを判定する。
        """

        if self.price_df.iloc[ref_day]['Close'] - self.price_df.iloc[ref_day]['Open'] > 0:
            return True
        else:
            return False

    def get_ma_vs_close(self, ma_days: int, ref_day: int) -> int:

        return self.price_df.iloc[ref_day][f"{'MA_' + str(ma_days)}_vs_Close"]
