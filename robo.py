from time import sleep

from iqoptionapi.stable_api import IQ_Option


class Robo:
    def __init__(
        self, id, email, password, asset="EURUSD", value=1, minutos=5, operations=10000
    ):
        self.email = email
        self.password = password
        self.asset = asset
        self.value = value
        self.minutos = minutos
        self.Iq = self.connection()
        #  self.weight_of_indicators = self.get_weight_of_indicators()
        self.operations = operations
        self.session_inputs = 0
        while self.operations != 0:
            self.operations -= 1
            self.indicators_result, self.result = self.get_indicators()
            self.buy_or_seel()
            sleep(1)
        print(
            f"""

        ENTRADAS REALIZADAS: {self.session_inputs}
        """
        )

    def connection(self):  # SUCESSO
        if self.email == " " and self.password == " ":
            while True:
                from getpass import getpass

                self.email = input("Email: ")
                self.password = getpass("Password: ")
                Iq = IQ_Option(self.email, self.password)
                check, reason = Iq.connect()
                if check == True:
                    print("Logado com sucesso!!")
                    break
                else:
                    print("Erro ao logar: ", reason)
        else:
            while True:
                Iq = IQ_Option(self.email, self.password)
                check, reason = Iq.connect()
                if check == True:
                    print("\n - Logado com sucesso!!")
                    break
                else:
                    print("\n - Erro ao logar: ", reason)
        return Iq

    def get_indicators(self):  # SUCESSO RETORNA (indicators_result, result)
        indicators = self.Iq.get_technical_indicators(self.asset)
        indicators_result = {}
        result = ""
        buy, sell, hold = 0, 0, 0
        for indicator in indicators:
            if indicator["candle_size"] == (self.minutos * 60):
                indicators_result[indicator["name"]] = indicator[
                    "action"
                ]  # hold, buy or sell
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
        return indicators_result, result

    def get_weight_of_indicators_and_sucess_rate(self):
        """
        return a list with 57 positions of weight_indicators,
        position 58 is right_operations
        position 59 is wrong_operations
        """

        database = open("database", "r")
        data = []
        for l in database:
            data.append(int(l))
        database.close()
        return data

    # change the weight of indicator according your sucess rate
    def change_weight_of_indicators(self):
        pass

    def buy_or_seel(self):
        if self.result == "buy":
            self.session_inputs += 1
            print(f"\n - {self.result} Operação acertiva...     COMPRANDO")
            self.Iq.buy(self.value, self.asset, "CALL", self.minutos)
        if self.result == "sell":
            self.session_inputs += 1
            print(f"\n - {self.result} Operação acertiva...     VENDENDO")
            self.Iq.buy(self.value, self.asset, "PUT", self.minutos)
        if self.result == "hold":
            print(f"\n - {self.result} Operação duvidosa...     ESPERANDO")
