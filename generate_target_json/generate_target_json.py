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
main_folder = r"C:\Users\User\Blau-Gelbes Kreuz Deutsch-Ukrainischer Verein e.V\BgK Finance " \
              r"- Documents\Integration"


def create_json_file(folder, json):
    guid = str(uuid.uuid4())
    file = open(folder+"\\"+guid+".json", "w")
    file.write(json)
    file.close()
    return guid


def process_paypal():
    def date_parser(str_date):
        return datetime.strptime(str_date, "%d.%m.%Y")
    paypal_file_name = '20221223_paypal_export.csv'
    paypal_file_name = '20221223_20221226_paypal_export.csv'
    # paypal_file_folder = main_folder + r"Paypal"
    paypal_file_location = main_folder + r"\Paypal\\" + paypal_file_name
    # paypal_processed_folder = main_folder + r"Paypal\Processed"
    paypal_processed_location = main_folder + r"\Paypal\Processed\\" + paypal_file_name
    paypal_write_folder = main_folder + r"\Paypal\JSON_Import"

    logging.info("-------------------Start of paypal processing-------------------")
    # Read CSV
    transaction_df = pd.read_csv(paypal_file_location, dtype={'Telefon': 'str'},
                                 parse_dates=['Datum'], date_parser=date_parser)
    transaction_df['Brutto'] = transaction_df['Brutto'].apply(locale.atof)
    transaction_df = transaction_entities.filter_df_paypal(transaction_df)
    transaction_df.fillna('', inplace=True)

    wpforms_df = get_wpforms_df()

    # Split CSV
    counter = 0
    for index, row in transaction_df.iterrows():
        paypal_transaction = transaction_entities.PaypalData(row)
        transaction_json = paypal_transaction.toJSON()
        add_wpforms_data(wpforms_df, paypal_transaction)
        file_name = create_json_file(paypal_write_folder, transaction_json)
        logging.info(f"File {file_name} was created for {paypal_transaction.source_name}, "
                     f"email {paypal_transaction.email}")
        counter += 1
        if counter == 20:
            break

    # Move CSV to Imported folder
    # shutil.move(paypal_file_location, paypal_processed_location)


def process_bank():
    def date_parser(str_date):
        return datetime.strptime(str_date, "%d.%m.%y")
    bank_file_name = '20220905-476346-umsatz.csv'
    bank_file_folder = main_folder + r"Bank"
    bank_file_location = bank_file_folder + '\\' + bank_file_name
    bank_processed_folder = main_folder + r"Bank\Processed"
    bank_processed_location = bank_processed_folder + '\\' + bank_file_name
    bank_write_folder = main_folder + r"Bank\JSON_Import"

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
                     f"iban {bank_transaction.cheque_number}")
        counter += 1
        if counter == 3:
            break

    # # Move CSV to Imported folder
    shutil.move(bank_file_location, bank_processed_location)


def process_stripe():
    def date_parser(str_date):
        return datetime.strptime(str_date, "%d.%m.%y")
    stripe_file_name = '20220905-476346-umsatz.csv'
    stripe_file_folder = main_folder + r"Stripe"
    stripe_file_location = stripe_file_folder + '\\' + stripe_file_name
    stripe_processed_folder = main_folder + r"Bank\Processed"
    stripe_processed_location = stripe_processed_folder + '\\' + stripe_file_name
    stripe_write_folder = main_folder + r"Bank\JSON_Import"

    logging.info("-------------------Start of bank processing-------------------")
    # Read CSV
    transaction_df = pd.read_csv(stripe_file_location, delimiter=";", decimal=',', thousands='.', encoding='Windows-1251',
                                 parse_dates=['Buchungstag'], date_parser=date_parser)
    transaction_df.fillna('', inplace=True)
    transaction_df = transaction_entities.filter_df_bank(transaction_df)

    # Split CSV
    counter = 0
    for index, row in transaction_df.iterrows():
        stripe_transaction = transaction_entities.StripeData(row)
        transaction_json = stripe_transaction.toJSON()
        print(transaction_json)
        file_name = create_json_file(stripe_write_folder, transaction_json)
        logging.info(f"File {file_name} was created for {stripe_transaction.source_name}, "
                     f"email {stripe_transaction.transaction_id}")
        counter += 1
        if counter == 3:
            break

    # # Move CSV to Imported folder
    shutil.move(stripe_file_location, stripe_processed_location)


def get_wpforms_df():
    def date_parser(str_date):
        return datetime.strptime(str_date, "%B %d, %Y %I:%M %p")
    locale.setlocale(locale.LC_ALL, 'en_US')
    wpforms_file = "wpforms-3114-Waerme-schenken-Spendeformular-2022-12-26-10-40-09.csv"
    wpforms_df = pd.read_csv(main_folder + r"\WPForms\\" + wpforms_file
                             , delimiter=",", decimal=',', thousands='.', encoding='utf-8',
                             parse_dates=['Entry Date'], date_parser=date_parser)
    wpforms_df = transaction_entities.filter_df_wpforms(wpforms_df)
    wpforms_df['Spendenbetrag'] = wpforms_df['Spendenbetrag'].map(lambda x: x.rstrip(' €'))
    wpforms_df['Spendenbetrag'] = wpforms_df['Spendenbetrag'].apply(locale.atof)
    return wpforms_df


def add_wpforms_data(wpforms_df, transaction_data):
    if transaction_data.email:
        print(transaction_data.email)
        wpforms_df = wpforms_df.loc[(wpforms_df["E-Mail"] == transaction_data.email)]
        wpforms_df = wpforms_df.loc[(wpforms_df["Entry Date"].dt.date == transaction_data.date)]
        if not wpforms_df.empty:
            print(wpforms_df.info())
            transaction_data.initWPForm(wpforms_df.iloc[0])
            transaction_json = transaction_data.toJSON()
            print(transaction_json)


locale.setlocale(locale.LC_ALL, 'de_DE')
logging_folder = main_folder + "\\Logs"
logging.basicConfig(filename=logging_folder+'\\' + timestamp_str + '_Transaction_process.txt',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

logging.info("Running Generating JSON files for Transactions")

process_paypal()
# process_bank()
logger = logging.getLogger('urbanGUI')

# def test_wpforms():
#     def date_parser(str_date):
#         return datetime.strptime(str_date, "%d.%m.%Y")
#     def date_parser_2(str_date):
#         return datetime.strptime(str_date, "%B %d, %Y %I:%M %p")
#     paypal_file_name = '20221223_20221226_paypal_export.csv'
#     paypal_file_folder = main_folder + r"\Paypal"
#     paypal_file_location = paypal_file_folder + '\\' + paypal_file_name
#     paypal_processed_folder = main_folder + r"\Paypal\Processed"
#     paypal_processed_location = paypal_processed_folder + '\\' + paypal_file_name
#     paypal_write_folder = main_folder + r"\Paypal\JSON_Import"
#
#     # Read CSV
#     transaction_df = pd.read_csv(paypal_file_location, dtype={'Telefon': 'str'},
#                                  parse_dates=['Datum'], date_parser=date_parser)
#     transaction_df['Brutto'] = transaction_df['Brutto'].apply(locale.atof)
#     transaction_df = transaction_entities.filter_df_paypal(transaction_df)
#     transaction_df.fillna('', inplace=True)
#
#     locale.setlocale(locale.LC_ALL, 'en_US')
#     wpforms_df = pd.read_csv(r"C:\Users\User\Blau-Gelbes Kreuz Deutsch-Ukrainischer Verein e.V\BgK Finance - "
#                              r"Documents\Integration\WPForms\wpforms-3114-Waerme-schenken-Spendeformular-2022-12-26-10-40-09.csv"
#                              , delimiter=",", decimal=',', thousands='.', encoding='utf-8',
#                              parse_dates=['Entry Date'], date_parser=date_parser_2)
#     wpforms_df = transaction_entities.filter_df_wpforms(wpforms_df)
#     wpforms_df['Spendenbetrag'] = wpforms_df['Spendenbetrag'].map(lambda x: x.rstrip(' €'))
#     wpforms_df['Spendenbetrag'] = wpforms_df['Spendenbetrag'].apply(locale.atof)
#
#     # print(wpforms_df.info())
#     # print(wpforms_df['Spendenbetrag'].head())
#
#     # Split CSV
#     counter = 0
#     for index, row in transaction_df.iterrows():
#         paypal_transaction = transaction_entities.PaypalData(row)
#         add_wpforms_data(wpforms_df, paypal_transaction)
#         counter += 1
#         if counter == 20:
#             break
# locale.setlocale(locale.LC_ALL, 'de_DE')
# test_wpforms()
