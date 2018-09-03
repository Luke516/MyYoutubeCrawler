# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import sqlite3
import json
import urllib.request
import string
import random
import datetime

def checkTableExists(dbcon, tablename):
    dbcur = dbcon.cursor()
    dbcur.execute("""
        SELECT COUNT(*)
        FROM sqlite_master 
        WHERE name = '{0}' AND  type='table'
        """.format(tablename.replace('\'', '\'\'')))
    if dbcur.fetchone()[0] == 1:
        dbcur.close()
        return True

    dbcur.close()
    return False

conn = sqlite3.connect('sql7.db')
c = conn.cursor()
print("Opened database successfully");

if checkTableExists(conn, "youtube_record"):
    print("Table already existed~");
else:
    c = conn.cursor()
    c.execute('''CREATE TABLE youtube_record
           (video_id        VARCHAR(50)      NOT NULL,
           video_title      VARCHAR(200)     NOT NULL,
           channel_id       VARCHAR(50)     NOT NULL,
           channel_title    VARCHAR(200),
           published_date   DATETIME);''')
    print("Table created successfully");
    conn.commit()


max_result = 50
API_KEY1 = 'AIzaSyBHHSqMtRCn6pb81TaeTumexKFrFaxdTxU'
API_KEY = 'AIzaSyDL-2qyhMKN2J6zqJ6kzvQHQQ8TI1AOD0Q'
API_KEY3 = 'AIzaSyCxFR5FbGjrRJcW_P-Qtn6wCiYWh5-BfyI'
random = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(3))

nextPageToken=""
prevPageToken=""

start_date = "03/10/18"
date_1 = datetime.datetime.strptime(start_date, "%m/%d/%y")
date_2 = date_1 - datetime.timedelta(days=1)
cur_date = date_2
next_date = cur_date + datetime.timedelta(minutes=59)
#print(cur_date.strftime("%Y-%m-%d"))
count=0

resultSet = {}

while cur_date < date_1:
    next_date = cur_date + datetime.timedelta(minutes=59)

    urlData = "https://www.googleapis.com/youtube/v3/search?key={}&maxResults={}&part=snippet&type=video&order=viewCount&publishedAfter={}&publishedBefore={}".format(API_KEY,max_result,cur_date.strftime("%Y-%m-%dT%H:%M:%SZ"),next_date.strftime("%Y-%m-%dT%H:%M:%SZ"))
    print(urlData)
    webURL = urllib.request.urlopen(urlData)
    data = webURL.read()
    encoding = webURL.info().get_content_charset('utf-8')
    results = json.loads(data.decode(encoding))
    
    with open('output.txt', 'ab') as out_file:
        if 'nextPageToken' in results:
            nextPageToken = results['nextPageToken']
            #out_file.write(nextPageToken.encode('utf-8'))
            #out_file.write('\n'.encode('utf-8'))
        
        if 'prevPageToken' in results:
            prevPageToken = results['prevPageToken']
            #out_file.write(prevPageToken.encode('utf-8'))
            #out_file.write('\n'.encode('utf-8'))
        
        for data in results['items']:
            videoId = (data['id']['videoId'])
            videoName = (data['snippet']['title'])
            videoName = videoName.replace('"','')
            channelId = (data['snippet']['channelId'])
            channelName = (data['snippet']['channelTitle'])
            channelName = channelName.replace('"','')
            publishedDate = (data['snippet']['publishedAt'])
            out_file.write(channelName.encode('utf-8'))
            out_file.write(" : ".encode('utf-8'))
            out_file.write(channelId.encode('utf-8'))
            out_file.write('\n'.encode('utf-8'))
            
            query = "INSERT INTO youtube_record (video_id, video_title, channel_id, channel_title, published_date) \
                        VALUES (\"" + videoId + "\", \"" + videoName + "\", \"" + channelId + "\", \"" + channelName + "\", \"" + publishedDate + "\" )"
            #print(query)
            c.execute(query);
            conn.commit()
            
            #resultSet[channelId] = channelName
            #store your ids
    
    if nextPageToken != "":
        end = 0
    else:
        end = 1
        
    while end == 0:
        urlData = "https://www.googleapis.com/youtube/v3/search?key={}&maxResults={}&part=snippet&type=video&order=viewCount&pageToken={}&publishedAfter={}&publishedBefore={}".format(API_KEY,max_result,nextPageToken,cur_date.strftime("%Y-%m-%dT%H:%M:%SZ"),next_date.strftime("%Y-%m-%dT%H:%M:%SZ"))
        print(urlData)
        webURL = urllib.request.urlopen(urlData)
        data = webURL.read()
        encoding = webURL.info().get_content_charset('utf-8')
        results = json.loads(data.decode(encoding))
        
        with open('output.txt', 'ab') as out_file:
            
            if 'prevPageToken' in results:
                prevPageToken = results['prevPageToken']
                #out_file.write("prevPageToken : ".encode('utf-8'))
                #out_file.write(prevPageToken.encode('utf-8'))
                
            #out_file.write(",  thisPageToken : ".encode('utf-8'))
            #out_file.write(nextPageToken.encode('utf-8'))
            
            if 'nextPageToken' in results:
                nextPageToken = results['nextPageToken']
                #out_file.write(",  nextPageToken : ".encode('utf-8'))
                #out_file.write(nextPageToken.encode('utf-8'))
                #out_file.write('\n'.encode('utf-8'))
            else:
                end = 1
                
            for data in results['items']:
                videoId = (data['id']['videoId'])
                videoName = (data['snippet']['title'])
                videoName = videoName.replace('"','')
                channelId = (data['snippet']['channelId'])
                channelName = (data['snippet']['channelTitle'])
                channelName = channelName.replace('"','')
                publishedDate = (data['snippet']['publishedAt'])
                out_file.write(channelName.encode('utf-8'))
                out_file.write(" : ".encode('utf-8'))
                out_file.write(channelId.encode('utf-8'))
                out_file.write('\n'.encode('utf-8'))
                
                query = "INSERT INTO youtube_record (video_id, video_title, channel_id, channel_title, published_date) \
                            VALUES (\"" + videoId + "\", \"" + videoName + "\", \"" + channelId + "\", \"" + channelName + "\", \"" + publishedDate + "\" )"
                #print(query)
                c.execute(query);
                conn.commit()
                
                #resultSet[channelId] = channelName
                #store your ids
    
    count += 1
    cur_date = cur_date + datetime.timedelta(hours=1)
    
print(count)

with open('channels.txt', 'ab') as out_file2:
    for key in resultSet:
        out_file2.write(key.encode('utf-8'))
        out_file2.write('\n'.encode('utf-8'))
        
conn.close()