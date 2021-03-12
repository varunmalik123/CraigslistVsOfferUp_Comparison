#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 22:58:38 2019

@author: kewang & Varun
"""

import pandas as pd
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

def meanPrice(dt):
    '''
    remove items with price range 100-1000 then find average price
    param: pd.dataframe
    return: float
    '''
    price = dt.Price
    price = price[(price <= 1000)]
    price = price[(price > 100)]
    
    return price.mean()

def condition(dt):
    '''
    return the number of items in different conditions, stored in a dict
    param: dataframe
    rtype: dict
    '''
    d = defaultdict(int)
    t1 = dt[(dt.Price > 100)]
    t2 = t1[(t1.Price <= 1000)]
    cd = t2.groupby('Attributes')
    
    print(cd.head())

    for g in cd.groups:
        d[g] = cd.groups[g].size
        
    return d


def conditionVSprice(dt):
    '''
    
    dt: dataframe
    d: dict(result from the function condition)
    return: dict
    '''
    
    c_vs_p = defaultdict(int)
    t1 = dt[(dt.Price > 100)]
    t2 = t1[(t1.Price <= 1000)] #removing items with price out of range
    cd = t2.groupby('Attributes')
    for condition in cd.groups:
        c_vs_p[condition] = dt.Price[cd.groups[condition]].mean()
    return c_vs_p

def newPost(dt,update):
    '''
    return the number of newly added post
    update: date of the generated file. e.g. the file was generated on 2019-11-24 then update = '2019-10-24'
    '''
    dt.postDate = dt.postDate.apply(lambda x: x[0:10]) # remove time stamp, leave only yr-month-day
    gp = dt.groupby('postDate').groups
    return gp[update].size

    
    
def contact(dt):
    '''
    return the number and portion of listings that have personal contact info
    '''
    t1 = dt[(dt.Price > 100)]
    t2 = t1[(t1.Price <= 1000)]    #filtering out listings with price out of price range
    all_listing = len(t2)
    t3 = t2[(t2.contactInfo)] 
    listing_with_contact = len(t3)
    portion = listing_with_contact / all_listing
    
    return listing_with_contact, portion

def pic(dt):
    '''
    return the number and portion of listings that have pictures
    '''
    
    t1 = dt[(dt.Price > 100)]
    t2 = t1[(t1.Price <= 1000)]
    all_listing = len(t2)
    t3 = t2[(t2.HasImage)]
    listing_with_image = len(t3)
    portion = listing_with_image / all_listing
    
    return listing_with_image, portion

def available(dt):
    '''
    return the number of listings and the portion of useful listings
    '''
    price = dt.Price
    all_listing = len(price)
    price = price[(price <= 1000)]
    price = price[(price > 100)]
    valid_listing = len(price)
    portion = valid_listing / all_listing
    
    return all_listing, portion

def distance(dt):
    
    t1 = dt[(dt.Price > 100)]
    t2 = t1[(t1.Price <= 1000)]
    under_ten = len(t2[(t2.distance < 10)])
    ten_to_fifty = len(t2[(t2.distance < 50)]) - under_ten
    fifty_above = len(t2[(t2.distance >= 50)])
    return under_ten, ten_to_fifty, fifty_above 

def plot_condition_bar(condition_dict):
    """
    Plot a bar graph of the condition of each phone with the height indicating the number in
    each respective group 

    :param condition_dict(dict): Input condition dictionary 
    :return :Bar Graph 
    """
    condition_list = []
    condition_value_list = []

    for key, value in condition_dict.items():
        condition_list.append(key)
        condition_value_list.append(value)

    index = np.arange(len(condition_list))
 
    plt.bar(x = index, height = condition_value_list)
    # # # Rotate x-labels
    plt.title("Condition")

    plt.xticks(index, condition_list, rotation=-30)
    plt.savefig("Condition_bar.png")




if __name__ == '__main__':
    



    filename = "/Users/varun/Desktop/ece143_fa19_bazhou_Varun_Angela_Frank-master/Craigslist_iphone 2019-11-24.csv"
    dt = pd.read_csv(filename)
    
    date_of_file = '2019-11-24'
    
    mean_price_of_the_day = meanPrice(dt)
    listings_under_diff_condition = condition(dt)
    conditon_versus_price = conditionVSprice(dt)
    num_of_new_post = newPost(dt,date_of_file)
    num_of_listing_with_contact, portion_contact = contact(dt)
    num_of_listing_with_image, portion_image = pic(dt)
    num_of_listing, portion_valid_listing = available(dt)
    under_ten, ten_to_fifty, fifty_above = distance(dt)
    
    # print('The mean price of the day is {}'.format(mean_price_of_the_day))

    ###### 

    # print("\n")
    
    condition(dt)


    # for key, values in listings_under_diff_condition.items(): 
    #     print(key, values)
    # print(listings_under_diff_condition["like new"])

    plot_condition_bar(listings_under_diff_condition)
    
    ######    
 

    # print(conditon_versus_price)
    
    # print("\n")

    # print('number of new post = {}'.format(num_of_new_post))
    