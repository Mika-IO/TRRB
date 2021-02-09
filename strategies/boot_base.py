# Logar
# Escolher asset
# Escolher tipo de opção e timeframe
from iqoptionapi.stable_api import IQ_Option


class BaseBoot:
    def __init__(self, email, password):
        self.email = email
        self.password = password

    def connect(self):
        if self.email == "" and self.password == "":
            while True:
                from getpass import getpass

                self.email = input("Email: ")
                self.password = getpass("Password: ")
                api = IQ_Option(self.email, self.password)
                check, reason = api.connect()
                if check:
                    break
                else:
                    print("\n - Erro ao logar: ", reason)
                    return "login error"
        else:
            while True:
                api = IQ_Option(self.email, self.password)
                check, reason = api.connect()
                if check:
                    break
                else:
                    print("\n - Erro ao logar: ", reason)
                    return "login error"
        return api

    def get_all_open_assets(self):
        ALL_Asset = self.api.get_all_open_time()
        all_open_assets = list(
            set(ALL_Asset["digital"].keys()).intersection(
                set(ALL_Asset["binary"].keys())
            )
        )
        return all_open_assets

    def get_payouts(self):
        assets = self.get_all_open_assets()
        all_binary_payouts = self.api.get_all_profit()
        digital_payouts = {}
        binary_payouts = {}
        for a in assets:
            binary = self.api.get_digital_current_profit(a, 1)
            digital = all_binary_payouts[a]["binary"]
            if type(binary) == float:
                digital_payouts[a] = binary
            if type(digital) == float:
                binary_payouts[a] = digital
        return {"binary_payouts": binary_payouts, "digital_payouts": digital_payouts}

    def get_best_payouts(self):
        payouts = self.get_payouts()
        binary_payouts = payouts["binary_payouts"]
        digital_payouts = payouts["digital_payouts"]
        old = 0
        greater_binary_payout = None
        for b in binary_payouts.keys():
            if binary_payouts[b] > old:
                greater_binary_payout = b
            old = binary_payouts[b]
        old = 0
        greater_digital_payout = None
        for d in digital_payouts.keys():
            if digital_payouts[d] > old:
                greater_digital_payout = d
            old = digital_payouts[d]
        return {
            "greater_binary_payout": greater_binary_payout,
            "greater_digital_payout": greater_digital_payout,
        }

    def choice_best_payout_asset(self):
        greater_payouts = self.get_best_payouts()
        greater_binary_payout = greater_payouts["greater_binary_payout"]
        greater_digital_payout = greater_payouts["greater_digital_payout"]

        if greater_binary_payout and greater_digital_payout:
            if greater_digital_payout > greater_binary_payout:
                return {"option": "digital", "asset": greater_digital_payout}
            elif greater_binary_payout > greater_digital_payout:
                return {"option": "binary", "asset": greater_binary_payout}
            else:
                return {"option": "digital", "asset": greater_digital_payout}
        elif greater_binary_payout:
            return {"option": "binary", "asset": greater_binary_payout}
        elif greater_digital_payout:
            return {"option": "digital", "asset": greater_digital_payout}
        else:
            return "no assets"

    def get_stop_loss_balance(self):
        balance = self.api.get_balance()
        stop_loss_balance = balance - self.stop_loss
        return stop_loss_balance

    def get_stop_gain_balance(self):
        balance = self.api.get_balance()
        stop_gain_balance = balance + self.stop_gain
        return stop_gain_balance
