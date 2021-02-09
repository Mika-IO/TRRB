from json import dumps
from time import sleep

from iqoptionapi.stable_api import IQ_Option

from .boot_base import BaseBoot


class Boot(BaseBoot):
    def __init__(
        self,
        email,
        password,
        asset="EURJPY-OTC",
        value=1,
        minutos=5,
        operations=10000,
    ):
        self.email = email
        self.password = password
        self.api = self.connect()
        self.asset = self.get_best_payouts()
        print(asset)
        self.value = value
        self.minutos = minutos
        #  self.weight_of_indicators = self.get_weight_of_indicators()
        self.operations = operations
        self.session_inputs = 0
        self.results = self.trading()

    def trading(self):
        while self.operations != 0:
            self.operations -= 1
            (
                self.sell,
                self.buy,
                self.hold,
                self.indicators_result,
                self.result,
            ) = self.get_indicators()
            if self.result:
                self.buy_or_seel()
            sleep(1)
        print(
            f"""

        ENTRADAS TOTAIS: {self.session_inputs}
        ENTRADAS WIN: 
        ENTRADAS LOSS
        """
        )
        return 0

    def get_indicators(self):
        indicators = self.api.get_technical_indicators(self.asset)
        if indicators["code"] == "no_technical_indicator_available":
            return 0, 0, 0, 0, 0
        indicators_result = {}
        result = ""
        buy, sell, hold = 0, 0, 0
        for indicator in indicators:
            if indicator["candle_size"] == (self.minutos * 60):
                indicators_result[indicator["name"]] = indicator["action"]
                if indicator["action"] == "buy":
                    buy += 1  # replace with indicator weights
                if indicator["action"] == "sell":
                    sell += 1  # replace with indicator weights
                if indicator["action"] == "hold":
                    hold += 1  # replace with indicator weights
        if hold / 3 > buy + sell:
            result = "hold"
        else:
            if buy > sell:
                result = "buy"
            if sell > buy:
                result = "sell"
        return sell, buy, hold, indicators_result, result

    def buy_or_seel(self):
        if self.result == "buy":
            self.session_inputs += 1
            print(f"\n - {self.result} Operação acertiva...     COMPRANDO")
            print(f" - SELL: {self.sell}    BUY: {self.buy}    HOLD: {self.hold}")
            op = self.api.buy(self.value, self.asset, "CALL", self.minutos)
            print(op)
        if self.result == "sell":
            self.session_inputs += 1
            print(f"\n - {self.result} Operação acertiva...     VENDENDO")
            print(f" - SELL: {self.sell}    BUY: {self.buy}    HOLD: {self.hold}")
            op = self.api.buy(self.value, self.asset, "PUT", self.minutos)
            print(op)
        if self.result == "hold":
            print(f"\n - {self.result} Operação duvidosa...     ESPERANDO")
            print(f" - SELL: {self.sell}    BUY: {self.buy}    HOLD: {self.hold}")
