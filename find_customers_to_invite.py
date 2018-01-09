import json

def open_customer_file(customers):
    """
    Opens customers text file, converts json into Python dictionary.

    """

    customers_list = []

    with open(customers) as customers_info:
        json_strings = customers_info.read().split('\n')
        for string in json_strings:
            customers_list.append(json.loads(string))

    return customers_list

print open_customer_file('customers.txt')