import json


def load_credentials(file):
    with open(file, "r", encoding="utf8") as f:
        credentials = json.load(f)
    return credentials["email"], credentials["password"]
