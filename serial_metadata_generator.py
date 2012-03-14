#Author: Nikhil Komawar 
#Affiliation: Rackspace Inc. USA
#email: nikhil.komawar@rackspace.com

"""
This script generates metadate for a list of customers to create a profile of
traffic hitting the servers.
"""
import sys
import threading
import time
import random
from datetime import datetime
from threading import Timer
from random import Random
import string
import datetime

"""
A set of global lists that are useful in writing the data in the metadata file
Keeping the lists global to avoid low overhead on memory
"""
profile_list = []
cust_list = []
sort_list = []
kv_dict = {}
cust = []

"""
Getting some date from the user to get a base layout of the profile
"""
def user_input(rate_of_requests,time_to_run, time_list):
    try:
        time_file = open('time_file.txt', 'r')
    except:
        print "time_file.txt could not be opened"
        quit()

    time_lines = time_file.readlines()
    time_file.close()
   
    for each_elem in time_lines:
        time_list = each_elem.split()

    no_profile_param = 3
    print "Enter whether you want to specify the rate of requests:\
        1: per hour\
        2: per minute\
        3: per second\n"
    rate_type = raw_input()
    if int(rate_type) == 1:
        div = 3600
    elif int(rate_type) == 2:
        div = 60
    elif int(rate_type) == 3:
        div = 1
    else:
        print "Sorry, you did not enter valid rate type!. Exiting...\n"
        quit()
   
    rate_of_requests = raw_input("Enter the number of requests you need.\n")
    rate_of_requests = int(rate_of_requests) / div
    time_to_run = raw_input("Enter the amount of time you want to run \
    the script\n")

    return rate_of_requests, time_to_run, time_list

"""
The config files are customer_list.txt and profile.txt
customer_list.txt must contain a list of customer IDs - one per line
profile.txt must contain in one per line:
    1. the expected fraction of api in the total requests
    2. the verb name
    3. the action on the verb
All these params must be separated by a single white space

These files may not contain any other information including comments.
"""
def get_config_data(no_customers,no_apis):
    try:
        customers = open('customer_list.txt', 'r')
    except:
        print "customer_list.txt could not be opened"
        quit()
    try:
        config_file = open('profile.txt', 'r')
    except:
        print "profile.txt could not be opened"
        quit()

    cust = customers.readlines()
    customers.close()

    for each_customer in cust:
        cust_list.append(int(each_customer))

    no_customers = len(cust_list)

    no_apis = 0
    lines = config_file.readlines()
    no_apis = len(lines)
    config_file.close()

    for line in lines:
        words = line.split()
        profile_list.append(words)

    return no_apis

"""
This function initialises the data in the lists which are use to write
to metadata.dat file
"""
def init_data(rand,no_apis,rate_of_requests):
    start = 0
    for it in range(0,no_apis):
        start += random.expovariate(float(profile_list[it][0]) * \
        rate_of_requests)
        sort_list.append(float(start))
        kv_dict[start] = it 

    sort_list.sort()

"""
The main function does the randomizing of data generation, keeping them in a
list sorted by data's timestamps and them writes to the metadata.dat file
"""
def main():
    rand = Random(999999)
    rate_of_requests = 0
    time_to_run = 0
    no_customers = 0
    no_apis = 0
    time_list = []

    #getting the user input
    rate_of_requests, time_to_run, time_list = \
    user_input(rate_of_requests,time_to_run, time_list)
    #updating the config data in the lists
    no_apis = get_config_data(no_customers,no_apis)
    #initialize the metadata lists
    init_data(rand,no_apis,rate_of_requests)
    
    meta = open('metadata.dat', 'a')
    time_now = datetime.datetime(int(time_list[0]),int(time_list[1]),\
    int(time_list[2]),int(time_list[3]),int(time_list[4]),int(time_list[5]))
    
    i=1
    while i <= int(rate_of_requests) * int(time_to_run):
        print_var = sort_list.pop(0)
        my_it = kv_dict[print_var]
        time_to_print = time_now + datetime.timedelta(0,print_var)
        """Writes the metadata generated into the metadata.dat file"""
        meta.write(str(time_to_print) + " " + str(profile_list[my_it][1]) +\
        " " + string.rstrip(str(cust_list[int(rand.random()*(no_customers))]))\
        + str(profile_list[my_it][2]) + "\n")
        """Update the metadata"""
        del kv_dict[print_var]
        start = print_var
        start += random.expovariate(float(profile_list[my_it][0]) * \
        rate_of_requests)
        sort_list.append(float(start))
        kv_dict[start] = my_it
        sort_list.sort()
        """Repeat until the required number of iterations are reached"""
        i+=1

    meta.close()
    
if __name__ == "__main__":
    main()
