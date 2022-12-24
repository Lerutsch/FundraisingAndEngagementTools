import nameparser
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
            salutation = 844060000
        elif gender == "male":
            salutation = 844060001

        # print(gender + ' ' + fullname)

        return salutation
    else:
        return 844060004


class DonorNameParser:
    def __init__(self, full_name):
        self.full_name = full_name

        parsed_name = nameparser.HumanName(self.full_name)
        self.first_name = str.title(parsed_name.first)
        self.last_name = str.title(parsed_name.last)
        self.middle_name = str.title(parsed_name.middle)
        self.title = str.title(parsed_name.title)

        self.salutation = get_salutation(full_name)

