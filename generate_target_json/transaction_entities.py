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


def format_field(value):
    if isinstance(value, datetime.date):
        return value.isoformat()
    else:
        return value.__dict__


class TransactionData:
    data_dict = {}
    mapping_dict = {}
    key = ''

    def toJSON(self):
        return json.dumps(self, default=format_field, sort_keys=True, indent=4)


class PaypalData(TransactionData):
    # Init from Series from DF from read CSV
    def __init__(self, df_row):
        self.gift_type = 'Paypal'
        self.source_name = df_row['Name']
        self.total_paid = df_row['Brutto']
        self.date = df_row['Datum'].date()
        self.phone = df_row['Telefon']
        self.email = df_row['Absender E-Mail-Adresse']
        self.transaction_id = df_row['Transaktionscode']

        self.key = 'email'

        donor_name_parser = DonorNameParser(self.source_name)
        self.first_name = donor_name_parser.first_name
        self.last_name = donor_name_parser.last_name
        self.salutation = donor_name_parser.salutation
        self.middle_name = donor_name_parser.middle_name
        self.title = donor_name_parser.title


class BankData(TransactionData):
    def __init__(self, df_row):
        self.gift_type = 'Wire or Transfer'
        self.source_name = df_row['Beguenstigter/Zahlungspflichtiger']
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
    gift_type = 'Stripe'
    data_dict = {'name': '', 'email': ''}
    key = 'email'


class DynamicsData(TransactionData):
    data_dict = {'name': '', 'email': ''}
    key = 'email'
