import json


def filter_df_paypal(df):
    df = df.loc[df["Brutto"] > 0]
    return df


class TransactionData:
    data_dict = {}
    mapping_dict = {}
    key = ''

    def __init__(self, df_row):
        self.source_name = ''
        self.first_name = ''
        self.last_name = ''
        self.salutation = ''
        self.total_paid = ''
        self.date = ''

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class PaypalData(TransactionData):
    # Init from Series from DF from read CSV
    def __init__(self, df_row):
        super().__init__(df_row)
        self.gift_type = 'Paypal'
        self.source_name = df_row['Name']
        self.first_name = df_row['Name']
        self.last_name = df_row['Name']
        self.salutation = ''
        self.total_paid = df_row['Brutto']
        self.date = df_row['Datum']
        self.phone = df_row['Telefon']
        self.email = df_row['Absender E-Mail-Adresse']
        self.transaction_id = df_row['Transaktionscode']

        self.key = 'email'


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
