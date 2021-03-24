from json import load

from trrb_strategies.boot_by_indicators import Boot
from trrb_core.usefull_functions import load_credentials

if __name__ == "__main__":
    email, password = load_credentials("userdata.json")
    by_indicators = Boot(email, password, 'PRATICE')
