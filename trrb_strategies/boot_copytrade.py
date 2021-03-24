import logging
from json import dumps
from time import sleep

from trrb_core.boot_base import BaseBoot

FORMAT = "%(levelname)s %(asctime)-15s %(filename)s %(module)s %(funcName)s %(message)s"
logging.basicConfig(format=FORMAT)
logger = logging.getLogger("root")
logger.setLevel("DEBUG")


class CopyButton(BaseBoot):
    def __init__(
        self, email, password, input=1, stop_gain=10, stop_loss=10, mode="PRACTICE"
    ):
        self.email = email
        self.password = password
        self.input = input
        self.stop_gain = stop_gain
        self.stop_loss = stop_loss
        self.option = ""
        self.asset = ""
        self.api = self.connect()
        self.mode = self.api.change_balance(mode)

    def get_best_traders_ids(self):
        ids = []
        ranking = self.api.get_leader_board("Worldwide", 1, 1000, 0)
        for r in ranking["result"]["positional"]:
            id = ranking["result"]["positional"][r]["user_id"]
            perfil_info = self.api.get_user_profile_client(id)
            if perfil_info["status"] == "online":
                ids.append(id)
        logging.info("Maiores traders encontrados com sucesso!")
        return ids

    def get_trading_setup(self):
        best_asset = self.choice_best_payout_asset()
        asset = best_asset["asset"]
        option = best_asset["option"]
        if best_asset["option"] == "binary":
            type_option = "live-deal-binary-option-placed"
        else:
            type_option = "PT1M"
        ids = self.get_best_traders_ids()
        setup = {
            "asset": asset,
            "type_option": type_option,
            "option": option,
            "input": self.input,
            "ids": ids,
            "balance_to_stop_loss": self.get_stop_loss_balance(),
            "balance_to_stop_gain": self.get_stop_gain_balance(),
        }
        print("\nSETUP\n", dumps(setup, indent=4), "\n")
        return setup

    def trading(self):
        setup = self.get_trading_setup()
        asset = setup["asset"]
        type_option = setup["type_option"]
        option = setup["option"]
        input = setup["input"]
        ids = setup["ids"]
        balance_to_stop_gain = setup["balance_to_stop_gain"]
        balance_to_stop_loss = setup["balance_to_stop_loss"]

        old = 0
        self.api.subscribe_live_deal(type_option, asset, option, 10)
        print("Trading...\n")
        while True:
            trades = self.api.get_live_deal(type_option, asset, option)
            if (
                (len(trades) > 0)
                and (old != trades[0]["user_id"])
                and (trades[0]["user_id"] in ids)
            ):
                if option == "binary":
                    print("iniciando uma operação binaria")
                    status, operation = self.api.buy(
                        input, asset, str(trades[0]["direction"]).lower(), 1
                    )
                    if status:
                        response, profit = self.api.check_win_v3(operation)
                        if response == "win":
                            print("Lucro", profit)
                        if response == "loose":
                            print("Prejuizo", profit)
                elif option == "digital":
                    print("iniciando uma operação digital")
                    status, operation = self.api.buy_digital_spot(
                        asset, input, str(trades[0]["instrument_dir"]).lower(), 1
                    )
                    while True:
                        if status:
                            status, profit = self.api.check_win_digital_v2(operation)
                            if status:
                                if profit > 0:
                                    print("Deu lucro", profit)

                                elif profit < 0:
                                    print("Deu preju", profit)
                            else:
                                status = True
                        else:
                            break

                balance = self.api.get_balance()
                if balance > balance_to_stop_gain:
                    print("Meta de ganhos atingida")
                    break
                elif balance < balance_to_stop_loss:
                    print("Stop loss atingido")
                    break
                old = trades[0]["user_id"]
            sleep(0.3)
        self.api.unscribe_live_deal(type_option, asset, option)

    def __str__(self):
        return self.email


if __name__ == "__main__":
    copy = CopyButton("mikaiofada@gmail.com", "ytbr5678")
    copy.tradding()
