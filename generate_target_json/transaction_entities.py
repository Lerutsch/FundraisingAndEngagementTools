import datetime
import json
from donor_name_parser import DonorNameParser


def filter_df_paypal(df):
    df = df.loc[df["Brutto"] > 0]
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
    gift_type = 'Paypal'
    data_dict = {'name': '', 'email': ''}
    key = 'email'


class StripeData(TransactionData):
    gift_type = 'Stripe'
    data_dict = {'name': '', 'email': ''}
    key = 'email'


class DynamicsData(TransactionData):
    data_dict = {'name': '', 'email': ''}
    key = 'email'
