import json
from random import choice

import names


with open("data/country_codes.json", "r") as f:
    country_codes = json.loads(f.read())


class UserData():
    def __init__(self) -> None:
        self.FULLNAME = names.get_full_name()

        self.FIRSTNAME = self.FULLNAME.split()[0]
        self.LASTNAME = self.FULLNAME.split()[1]

        self.COUNTRY_CODE = choice(country_codes)
