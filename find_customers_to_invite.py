import json
from math import radians, cos, sin, asin, sqrt

EARTH_RADIUS_IN_KM = 6371
INTERCOM_OFFICE = { 'latitude': 53.3381985, 'longitude': -6.2592576 }

def get_customer_objects(customers_data):
    """
    Opens customers text file, converts json into Python dictionary.

    """

    customers_list = []

    with open(customers_data) as customers_info:
        json_strings = customers_info.read().split('\n')
        for string in json_strings:
            customers_list.append(json.loads(string))

    return customers_list

# print open_customer_file('customers.txt')

def calculate_customer_distance_to_office(customer):

    office_lat, office_long = radians(INTERCOM_OFFICE['latitude']), \
                              radians(INTERCOM_OFFICE['longitude'])

    cust_lat, cust_long = radians(float(customer['latitude'])), \
                          radians(float(customer['longitude']))

    delta_long = abs(cust_long - office_long)
    delta_lat = abs(cust_lat - office_lat)
    
    # Haversine Formula
    x = (sin(delta_lat/2)**2
        + cos(office_lat)
        * cos(cust_lat)
        * sin(delta_long/2) ** 2)

    central_angle = 2 * asin(sqrt(x))

    return central_angle * EARTH_RADIUS_IN_KM


def get_customers_to_invite(customers_list):
    """
    Takes in list of customer objects and filters into new list
    of customers using distance calculation function.

    Returns a sorted list of nearby customers.
    """

    nearby_customers = [customer for customer in customers_list \
                       if calculate_customer_distance_to_office(customer) <= 100]

    sorted_invitations = sorted(nearby_customers, key=lambda customer: customer['user_id'])

    return sorted_invitations


def output_invitation_list(nearby_customers, guestlist_file):
    """
    Output results in a text file with customer names and user ids.

    """

    with open(guestlist_file, 'w') as guestlist:
        for customer in nearby_customers:
            guestlist.write(str(customer['user_id']) + ' ' + customer['name'] + '\n')

    return



all_customers = get_customer_objects('customers.txt')
invited = get_customers_to_invite(all_customers)
output_invitation_list(invited, 'guestlist.txt')
 

