import locale
import uuid
from datetime import datetime

import transaction_entities
import pandas as pd

locale.setlocale(locale.LC_ALL, 'de_DE')

# TD = transaction_entities.TransactionData()
# TD.salutation = 'salut'
# TD.date = '15.07.2022'
# TD.last_name = 'Lastbutnotleast'
#
# TDP = transaction_entities.PaypalData()
# TDP.salutation = 'salut_payp'
# TDP.date = '13.07.2022'
# TDP.last_name = 'Payp'
#
# print(TD.toJSON())
# print(TDP.toJSON())
# print(TDP.gift_type)


def create_json_file(folder, json):
    file = open(folder+"\\"+str(uuid.uuid4())+".json", "w")
    file.write(json)
    file.close()


def date_parser(str_date):
    return datetime.strptime(str_date, "%d.%m.%Y")


def process_paypal():
    paypal_file_location = r"C:\Users\OleksiiMakarenko\Blau-Gelbes Kreuz Deutsch-Ukrainischer Verein e.V\BgK Finance " \
                           r"- Documents\Integration\Paypal\Download.csv"
    paypal_write_folder = r"C:\Users\OleksiiMakarenko\Blau-Gelbes Kreuz Deutsch-Ukrainischer Verein e.V\BgK Finance " \
                          r"- Documents\Integration\Paypal\JSON_Import"
    # Read CSV
    # transaction_df = pd.read_csv(paypal_file_location, decimal=',', thousands='.')
    # custom_date_parser = lambda x: datetime.strptime(x, "%d.%m.%Y")
    # transaction_df = pd.read_csv(paypal_file_location, parse_dates=['Datum'], date_parser=custom_date_parser)
    transaction_df = pd.read_csv(paypal_file_location, dtype={'Telefon': 'str'},
                                 parse_dates=['Datum'], date_parser=date_parser)
    transaction_df['Brutto'] = transaction_df['Brutto'].apply(locale.atof)
    # transaction_df['Telefon'] = transaction_df['Telefon'].astype('str')
    # transaction_df['Brutto'] = transaction_df['Brutto'].apply(lambda x: x.replace('.', ''))
    # transaction_df['Brutto'] = transaction_df['Brutto'].apply(lambda x: x.replace(',', '.'))
    # transaction_df['Brutto'] = transaction_df['Brutto'].astype('float64')
    transaction_df = transaction_entities.filter_df_paypal(transaction_df)

    # print(transaction_df['Datum'])
    # Split CSV
    for index, row in transaction_df.iterrows():
        paypal_transaction = transaction_entities.PaypalData(row)
        transaction_json = paypal_transaction.toJSON()
        create_json_file(paypal_write_folder, transaction_json)
        break

        # Log result of file creation

    # Move CSV to Imported folder


process_paypal()
