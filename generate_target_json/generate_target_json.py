import locale
import time
import uuid
from datetime import datetime

import transaction_entities
import pandas as pd

import logging

import os
import shutil


timestamp_str = time.strftime("%Y%m%d-%H%M%S")


def create_json_file(folder, json):
    guid = str(uuid.uuid4())
    file = open(folder+"\\"+guid+".json", "w")
    file.write(json)
    file.close()
    return guid


# def date_parser(str_date):
#     return datetime.strptime(str_date, "%d.%m.%Y")


def process_paypal():
    def date_parser(str_date):
        return datetime.strptime(str_date, "%d.%m.%Y")
    paypal_file_name = '20221223_paypal_export.csv'
    paypal_file_folder = r"C:\Users\OleksiiMakarenko\Blau-Gelbes Kreuz Deutsch-Ukrainischer Verein e.V\BgK Finance " \
                           r"- Documents\Integration\Paypal"
    paypal_file_location = paypal_file_folder + '\\' + paypal_file_name
    paypal_processed_folder = r"C:\Users\OleksiiMakarenko\Blau-Gelbes Kreuz Deutsch-Ukrainischer Verein e.V\BgK " \
                                r"Finance - Documents\Integration\Paypal\Processed"
    paypal_processed_location = paypal_processed_folder + '\\' + paypal_file_name
    paypal_write_folder = r"C:\Users\OleksiiMakarenko\Blau-Gelbes Kreuz Deutsch-Ukrainischer Verein e.V\BgK Finance " \
                          r"- Documents\Integration\Paypal\JSON_Import"

    logging.info("-------------------Start of paypal processing-------------------")
    # Read CSV
    transaction_df = pd.read_csv(paypal_file_location, dtype={'Telefon': 'str'},
                                 parse_dates=['Datum'], date_parser=date_parser)
    transaction_df['Brutto'] = transaction_df['Brutto'].apply(locale.atof)
    transaction_df = transaction_entities.filter_df_paypal(transaction_df)
    transaction_df.fillna('', inplace=True)

    # Split CSV
    counter = 0
    for index, row in transaction_df.iterrows():
        paypal_transaction = transaction_entities.PaypalData(row)
        transaction_json = paypal_transaction.toJSON()
        file_name = create_json_file(paypal_write_folder, transaction_json)
        logging.info(f"File {file_name} was created for {paypal_transaction.source_name}, "
                     f"email {paypal_transaction.email}")
        counter += 1
        if counter == 3:
            break

    # Move CSV to Imported folder
    shutil.move(paypal_file_location, paypal_processed_location)


def process_bank():
    def date_parser(str_date):
        return datetime.strptime(str_date, "%d.%m.%y")
    bank_file_name = '20220905-476346-umsatz.csv'
    bank_file_folder = r"C:\Users\User\Blau-Gelbes Kreuz Deutsch-Ukrainischer Verein e.V\BgK Finance " \
                           r"- Documents\Integration\Bank"
    bank_file_location = bank_file_folder + '\\' + bank_file_name
    bank_processed_folder = r"C:\Users\User\Blau-Gelbes Kreuz Deutsch-Ukrainischer Verein e.V\BgK " \
                                r"Finance - Documents\Integration\Bank\Processed"
    bank_processed_location = bank_processed_folder + '\\' + bank_file_name
    bank_write_folder = r"C:\Users\User\Blau-Gelbes Kreuz Deutsch-Ukrainischer Verein e.V\BgK Finance " \
                          r"- Documents\Integration\Bank\JSON_Import"

    logging.info("-------------------Start of bank processing-------------------")
    # Read CSV
    transaction_df = pd.read_csv(bank_file_location, delimiter=";", decimal=',', thousands='.', encoding='Windows-1251',
                                 parse_dates=['Buchungstag'], date_parser=date_parser)
    transaction_df.fillna('', inplace=True)
    transaction_df = transaction_entities.filter_df_bank(transaction_df)

    # Split CSV
    counter = 0
    for index, row in transaction_df.iterrows():
        bank_transaction = transaction_entities.BankData(row)
        transaction_json = bank_transaction.toJSON()
        print(transaction_json)
        file_name = create_json_file(bank_write_folder, transaction_json)
        logging.info(f"File {file_name} was created for {bank_transaction.source_name}, "
                     f"email {bank_transaction.email}")
        counter += 1
        if counter == 3:
            break

    # # Move CSV to Imported folder
    shutil.move(bank_file_location, bank_processed_location)


locale.setlocale(locale.LC_ALL, 'de_DE')
logging_folder = r"C:\Users\OleksiiMakarenko\Blau-Gelbes Kreuz Deutsch-Ukrainischer Verein e.V\BgK Finance " \
               r"- Documents\Integration\Logs"
logging.basicConfig(filename=logging_folder+'\\' + timestamp_str + '_Transaction_process',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

logging.info("Running Generating JSON files for Transactions")

# process_paypal()
# process_bank()
logger = logging.getLogger('urbanGUI')
