import sys, json, doctest
from math import radians, cos, sin, asin, sqrt

EARTH_RADIUS_IN_KM = 6371
INTERCOM_OFFICE = { 'latitude': 53.3381985, 'longitude': -6.2592576 }


def get_all_customers(customers_file):
    """
    Opens customers text file and converts string into list of customers as 
    Python dictionaries.
    
    >>> get_all_customers('test.txt') == [{"animal": "dog", "name": "Bronco"}, {"animal": "cat", "name": "Garfield"}]
    True

    """

    all_customers = []

    with open(customers_file) as customers_info:
        json_strings = customers_info.read().split('\n')
        for string in json_strings:
            all_customers.append(json.loads(string))

    return all_customers


def calculate_customer_distance_to_office(customer):
    """
    Takes in a customer dictionary object with latitude and longitude keys
    and returns the distance of the customer from the Intercom Dublin office 
    using the Great Circle Distance Method and the Harversine Formula.
    
    >>> calculate_customer_distance_to_office({ 'latitude': 53.3381985, 'longitude': -6.2592576})
    0.0

    >>> int(calculate_customer_distance_to_office(test_input[2])) in range(int(0.95 * 4887), int(1.05 * 4887))
    True
    
    """

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


def choose_customers_to_invite(customers_list):
    """
    Takes in list of customer objects and filters into new list
    of customers using distance calculation function.

    Returns a sorted list of nearby customers.

    >>> choose_customers_to_invite([{'latitude': 41.49008, 'longitude': -71.312796}])
    []

    >>> choose_customers_to_invite(test_input) == [{'latitude': 53.1302756, 'user_id': 1, 'longitude': -6.2397222}, {'latitude': 53.2451022, 'user_id': 5, 'longitude': -6.238335}]
    True
    
    """

    nearby_customers = [customer for customer in customers_list \
                       if calculate_customer_distance_to_office(customer) <= 100]

    sorted_invitations = sorted(nearby_customers, key=lambda customer: customer['user_id'])

    return sorted_invitations


def output_invitation_list(nearby_customers, guestlist_file):
    """
    Outputs guestlist into a text file with customer names and user ids.

    """

    with open(guestlist_file, 'w') as guestlist:
        for customer in nearby_customers:
            guestlist.write(str(customer['user_id']) + ' ' + customer['name'] + '\n')

    return


test_input = [{'latitude': 53.2451022, 'longitude': -6.238335, 'user_id': 5},
              {'latitude': 53.1302756, 'longitude': -6.2397222, 'user_id': 1},
              {'latitude': 41.49008, 'longitude': -71.312796, 'user_id': 2}]


if __name__ == '__main__':
    all_customers = get_all_customers('customers.txt')
    invited = choose_customers_to_invite(all_customers)
    output_invitation_list(invited, 'guestlist.txt')

    doctest.testmod()
