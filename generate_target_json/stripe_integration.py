import stripe
import pandas as pd
import configparser
from flatten_json import flatten


def request_data(limit=100, starting_after="", ending_before=""):
    if starting_after and ending_before:
        transaction_list = stripe.Charge.list(limit=limit, starting_after=starting_after, ending_before=ending_before).data
    elif starting_after:
        transaction_list = stripe.Charge.list(limit=limit, starting_after=starting_after).data
    elif ending_before:
        transaction_list = stripe.Charge.list(limit=limit, ending_before=ending_before).data
    else:
        transaction_list = stripe.Charge.list(limit=limit).data
    return transaction_list


def get_new_transactions():
    charges_df = pd.read_csv("temp/charges_test.csv", index_col="id")
    ending_before = ""
    if not charges_df.empty:
        ending_before = charges_df.index[0]

    config = configparser.RawConfigParser()
    config.read('settings.ini')

    stripe.api_key = config.get('Stripe', 'stripe_api_key_test')

    # print(stripe.Customer.retrieve("cus_Mf1DqQ83qDiTFF"))
    # print(stripe.Customer.list(limit=3))
    # print(stripe.PaymentIntent.retrieve('pi_3MHpVAEBAzHmFz3E1Dkp72ud'))
    # print(stripe.Customer.retrieve('cus_Mf1DqQ83qDiTFF'))
    # print(stripe.Source.retrieve('src_1MMAdIEBAzHmFz3Eog0fK0rm'))
    # print(stripe.PaymentIntent.retrieve('pi_3MHpVAEBAzHmFz3E1Dkp72ud').charges.data[0].amount)
    # print(stripe.PaymentIntent.retrieve('pi_3MHpVAEBAzHmFz3E1Dkp72ud').charges.data[0].billing_details.name)
    # print(stripe.Charge.list().data)
    # print(stripe.Charge.list().data[0])

    transaction_list = request_data(ending_before=ending_before)

    if len(transaction_list) == 100:
        print("More than 100")
        last_transaction = transaction_list[len(transaction_list)-1]
        print(last_transaction)
        transaction_list_temp = request_data(starting_after=last_transaction, ending_before=ending_before)
        while len(transaction_list_temp) > 0:
            transaction_list += transaction_list_temp
            print(len(transaction_list))
            last_transaction = transaction_list[len(transaction_list)-1]
            transaction_list_temp = request_data(starting_after=last_transaction, ending_before=ending_before)

    if len(transaction_list):
        # list(map(lambda i: flatten(transaction_list, i), range(0, len(transaction_list))))
        # print(len(transaction_list))
        print(transaction_list[0])
        # TODO: flattening json (in particular billing_details)
        test = flatten(transaction_list[0])
        print(test)

        charges_df_new = pd.DataFrame.from_records(transaction_list)
        charges_df_new.set_index("id", inplace=True)
        charges_df_new["Object"] = transaction_list

        # print(charges_df.info())
        charges_df = pd.concat([charges_df, charges_df_new])
        # charges_df.append(charges_df_new)
        charges_df.sort_values("created", ascending=False, inplace=True)
        # print(charges_df.billing_details.address.city)
        # print(charges_df.info())
        # print(charges_df.head())

        # for index, row in charges_df.iterrows():
        #
        #     break
        # print(charges_df.info())
        # charges_df.to_csv("temp/charges_test.csv")
    else:
        print("No new records")


get_new_transactions()
