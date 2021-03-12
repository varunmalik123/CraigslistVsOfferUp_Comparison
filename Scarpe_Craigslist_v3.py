#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 14:53:18 2019

@author: kewang
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import datetime
import pandas as pd

def getHTMLText(url):
    try:
        r = requests.get(url, timeout = 30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return 'Exception!'
    
def nextPage(soup):
    '''
    return: next_page url
    '''    
    url = 'https://sandiego.craigslist.org'
    body = soup.body
    button = body.section.find('span', class_ = 'buttons')
    buttonnext = button.find('a', class_ = 'button next')

    url +=  buttonnext['href']

    return url
    
def singlePost(url):
    '''
    param: url
    return: list of attributes list[str]
    
    '''
    r = getHTMLText(url)
    soup = BeautifulSoup(r,'html.parser')
    section = soup.body.section.section.section
    attrs = section.find('p', class_ = 'attrgroup')

    res = [] #list of attributes
    try: 
        for a in attrs.find_all('span'):
            attr = ''
            for s in a:
                attr += s.string
            res.append(attr)
    except:
        pass
    
    contact = 'False'
    latitude = 0
    longitude = 0
    if section.find('p', class_ = 'postinginfo'):
        
        postID = section.find('p', class_ = 'postinginfo').string
        
        postingBody = section.section

        for c in postingBody.children:
            if 'Text' in c or 'text' in c or 'Call' in c or 'call' in c:
                contact = 'True'
            elif postingBody.a:
                contact = 'True'

    else:
        postID = 'None'
    if section.find('div', id = 'map'):
        s = section.find('div', class_ ="viewposting")
        latitude = s['data-latitude']
        longitude = s['data-longitude']
    
    return res, postID, contact, latitude, longitude

def fillItemList(text):
    '''
    param: text
    return: soup, list[list]
    
    
    '''
    soup = BeautifulSoup(text,'html.parser')
    body = soup.body
    for child in body.section.children:
        if child.name == 'form':
            form = child
        
    ct = form.find('div', class_ = 'content')
    item_list = ct.ul
    item_info = []

    for item in item_list.find_all('li'):
    
        item_title = item.p.a.string
     
        meta = item.p.find('span', class_ = 'result-meta')
        item_price = meta.span.string
        post_date = item.p.find('time')
        item_date = post_date['datetime']
        item_url = item.a['href']
        
        attr, postID, contact, latitude, longitude = singlePost(item_url) #attr = list[str], postID = str
        
        image = 'No' if len(item.a['class']) == 3 else 'Yes'
        name = item_title
        price = item_price
        postDate = item_date
        
        item_info.append([name, price, postDate, image, attr, postID, contact, latitude, longitude])
        
    return soup, item_info

def outputFile(d, path):
    '''
    param: d
    type: list[list]
    
    '''
    name, price, date, image, attr, postID, contact, latitude, longitude = [],[],[],[],[],[],[], [], []
    for i in d:
        name.append(i[0])
        price.append(i[1])
        date.append(i[2])
        image.append(i[3])
        attr.append(i[4])
        postID.append(i[5])
        contact.append(i[6])
        latitude.append(i[7])
        longitude.append(i[8])
    dataframe = pd.DataFrame({'Name': name, \
                              'Price': price, \
                              'postDate': date, \
                              'HasImage': image, \
                              'Attributes': attr, \
                              'postID': postID, \
                              'contactInfo': contact, \
                              'latitude': latitude, \
                              'longitude': longitude})
    
    dataframe.to_csv(path, index = True) 

 
def start(url):
   
    r = getHTMLText(url)
    time = datetime.datetime.now()
    out_path= '/Users/kewang/Desktop/ECE143/test_{}_{}.csv'.format(url[49:57], time)
    
    print('now processing page 1')
    s, d = fillItemList(r) #process first page

    for i in range(10):  
        try:           
            url = nextPage(s)
            r = getHTMLText(url)
            s_next, d_next = fillItemList(r)
            for i in d_next:
                d.append(i)
            s = s_next
            
            #print('now processing page {}'.format(i + 2))
        except:
            print('Running out of pages.')
            break
    outputFile(d, out_path)

if __name__ == '__main__':
    i = datetime.datetime.now()
    while True:
        url_iphonex = 'https://sandiego.craigslist.org/search/sss?query=iphone+x&sort=rel'     
        start(url_iphonex)
        
        print('finish round {}'.format(i))
        time.sleep(120) # scrape after 120s
        i = datetime.datetime.now()
    
    
    
   
