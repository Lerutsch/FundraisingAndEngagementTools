import os

import numpy as np
import pandas as pd
from enum import Enum
"contactid	firstname	lastname	fullname	emailaddress1	address1_line1	address1_line2	" \
"address1_city	description	msnfp_constituentnumber"


class Dependency(Enum):
    NOCONFLICT = 1
    MAINRECORD = 2
    CONFLICT = 3


def process_contact(contact_df, record_list, json_file):
    pd.set_option('display.max_columns', None)
    previous_contact = pd.DataFrame
    previous_contact_compare = pd.DataFrame
    main_record_id = ''
    for contactid in record_list:
        current_contact = contact_df.loc[contact_df['contactid'] == contactid]
        current_contact.reset_index(drop=True, inplace=True)
        current_contact_compare = current_contact[["emailaddress1",	"address1_line1", "address1_line2", "address1_city"]]

        if not previous_contact_compare.empty:
            compare_result = current_contact_compare.compare(previous_contact_compare)
            if compare_result.empty:
                # main_record = current_contact
                main_record_id = current_contact["contactid"][0]
                # print("No difference")
            else:
                count_current = current_contact_compare.count(axis=1)[0]
                count_previous = previous_contact_compare.count(axis=1)[0]
                print(count_current)
                print(count_previous)
                print(compare_result)
                if count_previous > count_current:
                    print(f'Main record previous - {previous_contact["msnfp_constituentnumber"]}')
                    # main_record = previous_contact
                    main_record_id = previous_contact["contactid"][0]
                else:
                    print(f'Main record current - {current_contact["msnfp_constituentnumber"]}')
                    # main_record = current_contact
                    main_record_id = current_contact["contactid"][0]
                    previous_contact = current_contact
                    previous_contact_compare = current_contact_compare
        else:
            previous_contact = current_contact
            previous_contact_compare = current_contact_compare

    contact_dict = {"main_record_id": main_record_id}
    counter = 1
    for contactid in record_list:
        if not contactid == main_record_id:
            create_json_merge_request(json_file, main_record_id, contactid)
            contact_dict[counter] = contactid
            counter += 1
            # contact = contact_df[contact_df['contactid'] == contactid]
            # index = contact.index
            # contact_df.loc[index, 'merge_result'] = f'Main record - {main_record_id}'

    return contact_dict


def create_json_merge_request(json_file, main_record_id, contactid):
    json_file.write('{')
    json_file.write('"Target":{"@odata.type":"Microsoft.Dynamics.CRM.contact","contactid":')
    json_file.write(f'{main_record_id}')
    json_file.write('},')
    json_file.write('"Subordinate":{"@odata.type":"Microsoft.Dynamics.CRM.contact","contactid":')
    json_file.write(f'{contactid}')
    json_file.write('},')
    json_file.write('"UpdateContent":{"@odata.type":"Microsoft.Dynamics.CRM.contact"},')
    json_file.write('"PerformParentingChecks":true')
    json_file.write('}\n')


def run():
    read_file = r"C:\Users\OleksiiMakarenko\OneDrive - Blau-Gelbes Kreuz Deutsch-Ukrainischer Verein e.V\IT\Dynamics Sales\Contact_merge.xlsx"
    # write_file = r"C:\Users\OleksiiMakarenko\OneDrive - Blau-Gelbes Kreuz Deutsch-Ukrainischer Verein e.V\IT\Dynamics Sales\Contact_merge_generated.xlsx"
    write_file = r"Contact_merge_generated.xlsx"
    json_path = "merge_contacts.csv"
    json_file = open(json_path, "w")
    # json_file.write("{")
    record_list = {}

    merge_contacts_df = pd.read_excel(read_file)
    current_name = ''
    counter = 0

    for index, row in merge_contacts_df.iterrows():
        if str(row['description']) == 'Bulk update, merge':
            counter += 1

            if current_name == '':
                current_name = row['fullname']
                record_list = [row['contactid']]
            elif current_name == row['fullname']:
                record_list.append(row['contactid'])
                # print(f"previous constituent: {current_name}")
            else:
                # print(f"new constituent: {row['fullname']}, previous list: {record_list}")
                contact_dict = process_contact(merge_contacts_df[merge_contacts_df['fullname'] == current_name], record_list, json_file)

                main_record_id = contact_dict.get('main_record_id')
                for key, value in contact_dict.items():
                    contact = merge_contacts_df[merge_contacts_df['contactid'] == value]
                    index = contact.index
                    if not key == 'main_record_id':
                        # merge_contacts_df[merge_contacts_df['contactid'] == value]
                        merge_contacts_df.loc[index, 'merge_result'] = f'Main record - {main_record_id}'
                    else:
                        merge_contacts_df.loc[index, 'merge_result'] = f'Main'

                record_list = [row['contactid']]
                current_name = row['fullname']

            # if counter == 40:
            #     break

    # json_file.write("}")
    merge_contacts_df.to_excel(write_file)
    json_file.close()


run()
