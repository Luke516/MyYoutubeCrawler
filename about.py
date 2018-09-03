# -*- coding: utf-8 -*-
"""
Created on Mon Aug 27 19:33:10 2018

@author: User
"""
import sqlite3
import urllib.request
from bs4 import BeautifulSoup
import re

def searchChannel(channel_id, conn):
    c = conn.cursor()
    
    urlData = "https://www.youtube.com/channel/{}/about".format(channel_id)
    #print(urlData)
    webURL = urllib.request.urlopen(urlData)
    data = webURL.read()
    
    soup = BeautifulSoup(data, 'lxml')

    links = soup.find_all(href=re.compile('^http.*(twitter|facebook)'))
    
    for tag in links:
        link = tag.get('href',None)
        if link is not None:
            print(link)
            query = "INSERT INTO links (channel_id, link) \
                        VALUES (\"" + channel_id + "\", \"" + link + "\" )"
            #print(query)
            c.execute(query);
            conn.commit()
            
conn = sqlite3.connect('sql7.db')
c = conn.cursor()
print("Opened database successfully");

cursor = c.execute("SELECT * from channels limit 2000") #42501
for row in cursor:
    channel_id = row[0]
    print("channel_id = ", channel_id)
    searchChannel(channel_id, conn)
conn.close()