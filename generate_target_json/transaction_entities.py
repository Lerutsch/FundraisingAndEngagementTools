import datetime
import json
from donor_name_parser import DonorNameParser


def filter_df_paypal(df):
    df = df.loc[df["Brutto"] > 0]
    df = df.loc[(df["Typ"] == 'Spendenzahlung') | (df["Typ"] == 'Abonnementzahlung')]
    return df


def filter_df_bank(df):
    df = df.loc[df["Betrag"] > 0]
    df = df.loc[(df["Buchungstext"] != 'RUECKUEBERWEISUNG')]
    return df


def filter_df_wpforms(df):
    df = df.loc[df["Payment Status"] == "Completed"]
    return df


def format_field(value):
    if isinstance(value, datetime.date):
        return value.isoformat()
    else:
        return value.__dict__


class TransactionData:
    def __init__(self):
        #WPForm
        self.address_ad = ""
        self.country = ""
        self.zip = ""
        self.city = ""
        self.salutation = ""
        self.payment_method = ""
        self.address = ""
        self.newsletter = 0
        self.designation = ""

    def toJSON(self):
        return json.dumps(self, default=format_field, sort_keys=True, indent=4)

    def initWPForm(self, wpform_row):
        if wpform_row['Subscribe to Newsletter']:
            self.newsletter = 1

        if not str(wpform_row['Adresse.1']) == 'nan':
            address = wpform_row['Adresse.1']
            address_list = address.split("\r\n")
            address_len = len(address_list)
            if address_len == 3:
                self.address = address_list[0]
                self.zip = address_list[1]
                self.country = address_list[2]
            elif address_len == 4:
                self.address = address_list[0]
                self.city = address_list[1]
                self.zip = address_list[2]
                self.country = address_list[3]
            elif address_len == 5:
                self.address = address_list[0]
                self.address_ad = address_list[1]
                self.city = address_list[2]
                self.zip = address_list[3]
                self.country = address_list[4]

        if not str(wpform_row['Anrede']) == 'nan':
            self.salutation = wpform_row['Anrede']
        self.payment_method = wpform_row['Zahlungsmethode']
        self.designation = wpform_row['Waerme schenken Paket']


class PaypalData(TransactionData):
    # Init from Series from DF from read CSV
    def __init__(self, df_row):
        super().__init__()
        self.gift_type = 'Paypal'
        self.source_name = df_row['Name']
        self.total_paid = df_row['Brutto']
        self.date = df_row['Datum'].date()
        self.phone = df_row['Telefon']
        self.email = df_row['Absender E-Mail-Adresse']
        self.transaction_id = df_row['Transaktionscode']
        self.purpose = df_row['Hinweis']

        self.key = 'email'

        donor_name_parser = DonorNameParser(self.source_name)
        self.first_name = donor_name_parser.first_name
        self.last_name = donor_name_parser.last_name
        self.salutation = donor_name_parser.salutation
        self.gender = donor_name_parser.gender
        self.middle_name = donor_name_parser.middle_name
        self.title = donor_name_parser.title


class BankData(TransactionData):
    def __init__(self, df_row):
        super().__init__()
        self.gift_type = 'Wire or Transfer'
        source_name = " ".join(df_row['Beguenstigter/Zahlungspflichtiger'].split())
        self.source_name = source_name
        self.total_paid = df_row['Betrag']
        self.date = df_row['Buchungstag'].date()
        self.purpose = df_row['Verwendungszweck']
        self.cheque_number = df_row['Kontonummer/IBAN']

        self.key = 'Kontonummer/IBAN'

        donor_name_parser = DonorNameParser(self.source_name)
        self.first_name = donor_name_parser.first_name
        self.last_name = donor_name_parser.last_name
        self.salutation = donor_name_parser.salutation
        self.middle_name = donor_name_parser.middle_name
        self.title = donor_name_parser.title


class StripeData(TransactionData):
    def __init__(self, df_row):
        super().__init__()
        self.gift_type = 'Stripe'
        self.source_name = df_row['Name']
        self.total_paid = df_row['Amount']
        self.date = df_row['Created (UTC)'].date()
        # self.purpose = df_row['Verwendungszweck']
        # self.cheque_number = df_row['Kontonummer/IBAN']
        self.email = df_row['Email']
        self.transaction_id = df_row['id']

        self.key = 'email'

        donor_name_parser = DonorNameParser(self.source_name)
        self.first_name = donor_name_parser.first_name
        self.last_name = donor_name_parser.last_name
        self.salutation = donor_name_parser.salutation
        self.middle_name = donor_name_parser.middle_name
        self.title = donor_name_parser.title


class DynamicsData(TransactionData):
    data_dict = {'name': '', 'email': ''}
    key = 'email'
