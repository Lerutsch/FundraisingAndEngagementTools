import nameparser
import requests


def get_gender(fullname):
    if (len(fullname.split())) < 4:
        gender = ""
        firstname = nameparser.HumanName(fullname).first

        if firstname:
            response = requests.get("https://api.genderize.io/?apikey=2ad36a85c5c98005467816be0b816c0b&name=" + firstname)

            data = response.json()
            if data['probability'] > 0.9:
                gender = data['gender']

        gender_int = 844060004
        if gender == "female":
            gender_int = 844060000
        elif gender == "male":
            gender_int = 844060001

        # print(gender + ' ' + fullname)

        return gender_int
    else:
        return 844060004


def get_salutation(gender):
    if gender == 844060000:
        return "Frau"
    elif gender == 844060001:
        return "Herr"


class DonorNameParser:
    def __init__(self, full_name):
        self.full_name = full_name

        parsed_name = nameparser.HumanName(self.full_name)
        self.first_name = str.title(parsed_name.first)
        self.last_name = str.title(parsed_name.last)
        self.middle_name = str.title(parsed_name.middle)
        self.title = str.title(parsed_name.title)

        self.gender = get_gender(full_name)
        self.salutation = get_salutation(self.gender)

