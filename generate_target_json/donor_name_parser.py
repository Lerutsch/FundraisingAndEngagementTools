import math

import nameparser
import numpy as np
import pandas as pd
import requests


def get_salutation(fullname):
    if (len(fullname.split())) < 4:
        gender = ""
        firstname = nameparser.HumanName(fullname).first

        if firstname:
            response = requests.get("https://api.genderize.io/?apikey=2ad36a85c5c98005467816be0b816c0b&name=" + firstname)

            data = response.json()
            if data['probability'] > 0.9:
                gender = data['gender']

        salutation = ""
        if gender == "female":
            salutation = "Frau"
        elif gender == "male":
            salutation = "Herr"

        # print(gender + ' ' + fullname)

        return salutation


class DonorNameParser:
    def __init__(self, full_name):
        self.full_name = full_name

        parsed_name = nameparser.HumanName(self.full_name)
        self.first_name = str.title(parsed_name.first)
        self.last_name = str.title(parsed_name.last)
        self.middle_name = str.title(parsed_name.middle)
        self.title = str.title(parsed_name.title)

        self.salutation = get_salutation(full_name)

    def get_first_name(self):
        return

    def get_last_name(self):
        return

    def get_salutation_name(self):
        return

