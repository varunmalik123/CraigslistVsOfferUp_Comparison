# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from urllib.request import urlopen
from selenium import webdriver
import re
import time
import os
import pandas as pd
import datetime


def get_id(url):
    ptn_url = r"\d+"
    item_id = re.search(ptn_url, url).group(0)

    return item_id


def get_title(soup):
    title_soup = soup.find("h1", {"class": "_t1q67t0 _1juw1gq"})
    title = title_soup.get_text()
    print(f'{title}')
    return title


def get_value(soup):
    value_soup = soup.find("span", {"class": "_ckr320"})
    ptn_money = r"(?<=\$).+" # the pattern to find anything after the dollar sign
    value = re.search(ptn_money, value_soup.get_text()).group(0) if (value_soup is not None) else 'Sold!'
    print(f'{value}')
    if value != 'Sold!': # if the value is actuall number, we convert it to number types
        value = value.replace(',','') # in order to correctly recognize comma-separated price like $1,000 or $1,000,000
        money = int(value) if value.isdigit() else float(value) # money will be of type int or float instead of str
    else:
        money = value # if the value is a string 'Sold!', then money is the same
    return value, money


def get_condition(soup):
    condition_soup = soup.find("span", {"data-test": "item-condition"})
    condition = condition_soup.get_text() if (condition_soup is not None) else 'No Condition INFO!'
    print(f'{condition}')

    return condition


def get_description(soup):
    description_soup = soup.find("div", {"data-test": "item-description"})
    description = description_soup.get_text() if (description_soup is not None) else 'No Description!'
    print(f'{description}')

    return description


def get_picture(soup):
    picture_soup = soup.find_all("img", {"class": "_fk4cz1", "src": re.compile("https://photos\.offerup\.com/.")})
    pic_num = len(picture_soup)
    pic_urls = []
    if pic_num != 0:
        for i in range(len(picture_soup)):
            pic_urls.append(picture_soup[i]['src'])
    print(f'Picture number is: {pic_num}')
    return pic_num, pic_urls


def get_shipping(soup):
    delivery_soup = soup.find("span", {"class": "_147ao2d8 hidden-xs _149pqlo", "data-name": "delivery-info"})
    shipping_soup = soup.find("span", {"class": "_1v68mn6s _17axpax", "data-name": "shipping-text"})
    # get the delivery info text
    delivery = delivery_soup.get_text() if (delivery_soup is not None) else 'No delivery INFO!'
    # get the shipping info text
    shipping = shipping_soup.get_text() if (shipping_soup is not None) else 'No shipping INFO!'

    # pattern to decide pick-up distance in integer
    ptn_dist = r"\d+|a.mile"
    # pattern to decide shipping location & price (when only delivery option is available)
    ptn_ship_loc_price = r"(?<=from.).+"
    # pattern to decide shipping price (when both delivery and pick-up options are available)
    ptn_ship_price = r"(?<=for..).+"
    # pattern to decide whether shipping included
    # ptn_pick = r"^Local pickup"

    print('shipping is: ', shipping)
    print('delivery is: ', delivery)

    distance = None
    ship_loc = None
    ship_price = None

    if delivery != 'No delivery INFO!':
        print('delivery INFO is: ', delivery)
        distance = re.search(ptn_dist, delivery).group(0)
        if distance.isdigit():
            distance = int(re.search(ptn_dist, delivery).group(0))
        else:
            distance = 1
        print(f'The distance for pick-up is: {distance}')

    if shipping != 'No shipping INFO!' and delivery != 'No delivery INFO!':
        ship_price = re.search(ptn_ship_price, shipping).group(0)
        print(f'The shipping price is {ship_price}')

    if shipping != 'No shipping INFO!' and delivery == 'No delivery INFO!':
        ship_loc_price = re.search(ptn_ship_loc_price, shipping).group(0)
        ship_loc = ship_loc_price.split(' for $')[0]
        ship_price = ship_loc_price.split(' for $')[1]
        print('ship_price is: ', ship_price)
        print(f'The seller\'s location is: {ship_loc}')

    return delivery, shipping, distance, ship_loc, ship_price


def get_location(soup, ship_loc):
    location_soup = soup.find("a", {"class": "_g85abvs _133jvmu8"})
    # when the product has shipping option
    if ship_loc is not None:
        location = ship_loc
        city, state = location.split(',', 1)
        print(f'{location}')
        return location, city, state
    # when pick-up is the option
    else:
        location = location_soup.get_text() if (location_soup is not None) else 'No location INFO!'
        if location != 'No location INFO!':
            city, state = location.split(',', 1)
            print(f'{location}')
            return location, city, state
        else:
            print(f'{location}')
            city = None
            state = None
            return location, city, state


def get_time(soup):
    time_soup = soup.find("div", {"class": "_147ao2d8"})
    time_text = time_soup.get_text() if (time_soup is not None) else 'Unknown Time!'

    ptn_time = r"\d+\s\w+\s"
    post_time = re.search(ptn_time, time_text).group(0)
    time_num, time_unit = post_time.split(' ', 1)
    print(time_num + ' ' + time_unit + 'ago')
    return post_time


def start_scrap(item_choice,base_url,keyword_choice,scroll_times,driver_addr):

    # Base_url is the main target webpage
    item_name_list = ["IPhoneX",
                      "SamsungGalaxyS8"]
    item_name = item_name_list[item_choice]
    
    keywordurl_list = ["/search/?q=iphone%20x&delivery_param=s_p&radius=50&price_min=100&price_max=",
                       "/search/?q=samsung%20galaxy%20s8&delivery_param=s_p&radius=50&price_min=100"]
    keyword_url = keywordurl_list[keyword_choice]
    
    search_results = []
    search_url = base_url + keyword_url  # starting point of scraping
    
    cwd = os.path.abspath(os.path.dirname(__file__))
    path_driver = cwd + driver_addr
    browser = webdriver.Chrome(path_driver)
    browser.get(search_url)
    browser.implicitly_wait(10)
    
    try:
        browser.refresh()  # refresh
        print('Refresh successfully')
    except Exception as e:
        print("Exception found", format(e))
    
    for _ in range(scroll_times):
        # execute_script will scroll the page down to the bottom
        browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        time.sleep(5)  # sleep a little while to avoid delay or conflict
    
    print("Search Starts")
    # print(browser.page_source)
    soup = BeautifulSoup(browser.page_source, features='lxml')  # BF4 analysis
    print("Search Finished!")
    
    # get all the item urls
    sub_urls = soup.find_all("a", {"class": "_109rpto _1anrh0x", "href": re.compile("/item/detail/\d+/")})
    sub_urls += soup.find_all("a", {"class": "_109rpto db-item-tile", "href": re.compile("/item/detail/\d+/")})
    if len(sub_urls) != 0:
        for i in range(len(sub_urls)):
            search_results.append(sub_urls[i]['href'])
    else:
        # no valid sub link found
        pass
    print(search_results)
    
    item_id_list = []
    title_list = []
    price_list = []
    condition_list = []
    description_list = []
    number_of_pic_list = []
    delivery_list = []
    shipping_list = []
    distance_list = []
    ship_loc_list = []
    ship_price_list = []
    location_list = []
    city_list = []
    state_list = []
    time_list = []
    
    for items in search_results:
        full_url = base_url + items
        print(f'\nLoading Url: {full_url}')
        sub_html = urlopen(full_url).read().decode('utf-8')
        sub_soup = BeautifulSoup(sub_html, features='lxml')
        print("Loading Item Finished!")
    
        print("Getting ID!")
        item_id = get_id(items)
        item_id_list.append(item_id)
    
        print("Getting Title!")
        title = get_title(sub_soup)
        title_list.append(title)
    
        print("Getting Value!")
        _, price = get_value(sub_soup)
        price_list.append(price)
    
        print("Getting Item Condition!")
        condition = get_condition(sub_soup)
        condition_list.append(condition)
    
        print("Getting Item Description!")
        description = get_description(sub_soup)
        description_list.append(description)
    
        print("Getting Item Picture")
        number_of_pic, _ = get_picture(sub_soup)
        number_of_pic_list.append(number_of_pic)
    
        print("Getting Shipping INFO!")
        delivery, shipping, distance, ship_loc, ship_price = get_shipping(sub_soup)
        delivery_list.append(delivery)
        shipping_list.append(shipping)
        distance_list.append(distance)
        ship_loc_list.append(ship_loc)
        ship_price_list.append(ship_price)
    
        print("Getting Location!")
        location, city, state = get_location(sub_soup, ship_loc)
        location_list.append(location)
        city_list.append(city)
        state_list.append(state)
    
        print("Getting Time!")
        post_time = get_time(sub_soup)
        time_list.append(post_time)
    
    print(f'We have scraped {len(search_results)} products on OfferUp.')
    
    try:
        browser.close()
    except:
        print('Browser already closed!')
        pass
    
    dataframe = pd.DataFrame({"Item ID": item_id_list,
                              "Title": title_list,
                              "Price": price_list,
                              "Condition": condition_list,
                              "Description": description_list,
                              "Number_of_pictures": number_of_pic_list,
                              "Delivery": delivery_list,
                              "Shipping": shipping_list,
                              "Distance": distance_list,
                              "Ship_Location": ship_loc_list,
                              "Ship_Price": ship_price_list,
                              "Location": location_list,
                              "City": city_list,
                              "State": state_list,
                              "Time": time_list})
    dataframe = dataframe.drop_duplicates(subset='Item ID')
    scrap_time = datetime.datetime.now()
    out_path= './{}_{}_Result_Offerup.csv'.format(item_name,scrap_time)
    dataframe.to_csv(out_path, index=True)

if __name__ == '__main__':
    import argparse
    
    item_choice=1
    base_url="https://offerup.com"
    scroll_times=10
    driver_addr='/macos_chromedriver'
    
    parser = argparse.ArgumentParser(description='define the url, search keyword, webdriver and scroll times')
    parser.add_argument("--item",default=item_choice,help="the item we search about",type=int)
    parser.add_argument("--base",default=base_url,help="the base offerup url",type=str)
    parser.add_argument("--scroll",default=scroll_times,help="the number of page to go over",type=int)
    parser.add_argument("--driver",default=driver_addr,help="the web driver address",type=str)
    
    args = parser.parse_args()
        
    start_scrap(args.item,args.base,args.item,args.scroll,args.driver)
    
