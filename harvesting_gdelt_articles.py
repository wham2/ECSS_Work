# -*- coding: utf-8 -*-
"""
Spyder Editor
This code will pull 10 article urls from each quarter of Calendar Year 2020 for two political figures from the GDELT dataset. Then we pull the full article, it's title, it's image, and the image seen date and compile them into a large matrix for processing with AI/ML. 

"""
import urllib
import requests
import io
import os, sys

names=["trump", "putin"]
articles_per_quarter=10

# establish content breadth
CY20Q1_trumplink ="https://api.gdeltproject.org/api/v2/doc/doc?query=imagewebtag:%22donald%20trump%22&mode=artlist&startdatetime=20200101000000&enddatetime=20200331235959&sourcelang:english&format=JSON&maxrecords=10"
CY20Q2_trumplink ="https://api.gdeltproject.org/api/v2/doc/doc?query=imagewebtag:%22donald%20trump%22&mode=artlist&startdatetime=20200401000001&enddatetime=20200630235959&sourcelang:english&format=JSON&maxrecords=10"
CY20Q3_trumplink ="https://api.gdeltproject.org/api/v2/doc/doc?query=imagewebtag:%22donald%20trump%22&mode=artlist&startdatetime=20200701000001&enddatetime=20200816000000&sourcelang:english&format=JSON&maxrecords=10"

CY20Q1_putinlink ="https://api.gdeltproject.org/api/v2/doc/doc?query=imagewebtag:%22vladimir%20putin%22&mode=artlist&startdatetime=20200101000000&enddatetime=20200331235959&sourcelang:english&format=JSON&maxrecords=10"
CY20Q2_putinlink ="https://api.gdeltproject.org/api/v2/doc/doc?query=imagewebtag:%22vladimir%20putin%22&mode=artlist&startdatetime=20200401000001&enddatetime=20200630235959&sourcelang:english&format=JSON&maxrecords=10"
CY20Q3_putinlink ="https://api.gdeltproject.org/api/v2/doc/doc?query=imagewebtag:%22vladimir%20putin%22&mode=artlist&startdatetime=20200701000001&enddatetime=20200816000000&sourcelang:english&format=JSON&maxrecords=10"


links_trump = [CY20Q1_trumplink, CY20Q2_trumplink, CY20Q3_trumplink]
links_putin = [CY20Q1_putinlink, CY20Q2_putinlink, CY20Q3_putinlink]

# define containers

#links = [CY20Q1_link]
article_list_trump=[]
article_text_trump=[]
article_images_trump=[]

article_list_putin=[]
article_text_putin=[]
article_images_putin=[]

# establish initial containers
art_sub_sections=[]
full_article=[]
bad_articles_trump={} # to view these use bad_articles_trump.items()
bad_articles_putin={}

for i,v in enumerate(links_trump):
    #print(i,v)
    response = requests.get(v).json()
    article_list_trump = article_list_trump + response['articles']
    print(i, "length of trump article list is : ", len(article_list_trump))
    
for i,v in enumerate(links_putin):
    #print(i,v)
    response = requests.get(v).json()
    article_list_putin= article_list_putin + response['articles']
    print(i,"length of putin article list is : ", len(article_list_putin))
    
# now we have two lists of articles with images from 2020, one for Trump and the other for Putin

""" 
a single record in JSON format looks like this :

{'title': 'title as text', 'socialimage': 'https:...', 'url':'https:...', 'sourcecountry': 'United States', 'seendate': '20200109T201500Z', 'url_mobile': '', 'domain': 'news.yahoo.com', 'language': 'English'}

As you can see, it is a dictionary

>>> article_list_trump[0]
{'title': 'It looks like Iran is ready to start bombing its fake aircraft carrier again', 'socialimage': 'https://s.yimg.com/ny/api/res/1.2/93relPXP9E1iH7ErLB9K6g--/YXBwaWQ9aGlnaGxhbmRlcjt3PTEyODA7aD02NDA-/https://s.yimg.com/uu/api/res/1.2/9Teu..o2Bs5PxtN6b76xSA--~B/aD00ODA7dz05NjA7c209MTthcHBpZD15dGFjaHlvbg--/https://media.zenfs.com/EN/business_insider_articles_888/7c6a7dcb460bbd70dff3a8a4719289cd', 'url': 'https://news.yahoo.com/looks-iran-ready-start-bombing-183724929.html', 'sourcecountry': 'United States', 'seendate': '20200109T201500Z', 'url_mobile': '', 'domain': 'news.yahoo.com', 'language': 'English'}

So to get the url or the title just use dictionary format:

>>> article_list_trump[0]['url']
'https://news.yahoo.com/looks-iran-ready-start-bombing-183724929.html'
>>> article_list_trump[0]['title']
'It looks like Iran is ready to start bombing its fake aircraft carrier again'
>>> article_list_trump[0]['socialimage']
'https://s.yimg.com/ny/api/res/1.2/93relPXP9E1iH7ErLB9K6g--/YXBwaWQ9aGlnaGxhbmRlcjt3PTEyODA7aD02NDA-/https://s.yimg.com/uu/api/res/1.2/9Teu..o2Bs5PxtN6b76xSA--~B/aD00ODA7dz05NjA7c209MTthcHBpZD15dGFjaHlvbg--/https://media.zenfs.com/EN/business_insider_articles_888/7c6a7dcb460bbd70dff3a8a4719289cd'

"""

# next lets try to get the actual article text and image from each list entry and put those in another list
    
import requests
import shutil
import imageio
import visvis as vv
import PIL
from PIL import Image
from urllib.request import urlopen
from urllib.request import urlretrieve
from pyquery import PyQuery as pq #this library is why you need to use python 3.5
from lxml import etree


# establish header for 'get' request to help legitimize our ask
headers = {'user-agent': 'Mozilla/Firefox 79.0 (OMEN by HP; Intel Core i7 Windows 10)'}
# response = urlopen('https://news.yahoo.com/residents-turned-arizona-purple-made-113109884.html').read() 

# loop through the article_list_trump
for k in range(len(article_list_trump)):
   response=requests.get(article_list_trump[k]['url'], stream=True, headers = headers, timeout = 5)
   # need an error handling routine to handle when there is no article <Response [404]>
   # to skip the rest of this code
   
   if response.status_code != 200:
       #skip all the good code and just increment the bad url counter
       #bad_record=[k:str(article_list_trump[k]['title']),str(article_list_trump[k]['url'])]
       bad_articles_trump[k]=article_list_trump[k]['title']
   else:
       #since the response has legitimate information, lets store it
       text_response = urlopen(article_list_trump[k]['url']).read()
       # Open the url image, set stream to True, this will return the stream content.
       image_response = requests.get(article_list_trump[k]['socialimage'], stream = True)
       image_bytes = io.BytesIO(image_response.content)
       img = Image.open(image_bytes)
       #img.show() #this lets you see the .jpg image in a separate window
    
       docTree=pq(text_response)
       #docTree.find('title').text()
       #docTree.find('p:eq(0)').text()
       #docTree.find('p:eq(2)').text()
    
       #[i.text() for i in docTree.items('p')] #iterates through all <p></p> tags
    
       art_sub_sections=[i.text() for i in docTree.items('p')] #creates a list of all text    sections of the article separated by commas
    
       #art1[0]+' '+art1[1] # constructs the first two subsections of the article as a string
    
       full_article=[] #create a location to store the full article (without being divided by <p> <\p> tags
    
       for w in range(len(art_sub_sections)):
          full_article = str(full_article) + ' ' + str(art_sub_sections[w])
       # now the full article is in full_article[0] as text
    
       article_text_trump.append(full_article)
       article_images_trump.append(img)
       # to show the article images use
       #article_images_trump[4].show()
       # to see the article text use
       # article_text_trump[4]
   
#end the loop

print('Length of valid article list for Trump is: ', len(article_text_trump))

# loop through the article_list_putin
for k in range(13,len(article_list_putin)):
   response=requests.get(article_list_putin[k]['url'], stream=True, headers = headers, timeout = 5)
   # need an error handling routine to handle when there is no article <Response [404]>
   # to skip the rest of this code
   # note, I was not able to get articles for k=7, 11, and 12 so had do change the range of the loop
   
   if response.status_code != 200:
       #skip all the good code and just increment the bad url counter
       #bad_record=[k:str(article_list_trump[k]['title']),str(article_list_trump[k]['url'])]
       bad_articles_putin[k]=article_list_putin[k]['title']
   else:
       #since the response has legitimate information, lets store it
       text_response = urlopen(article_list_putin[k]['url']).read()
       # Open the url image, set stream to True, this will return the stream content.
       
       image_response = requests.get(article_list_putin[k]['socialimage'], stream = True)
       image_bytes = io.BytesIO(image_response.content)
       img = Image.open(image_bytes)
       #img.show() #this lets you see the .jpg image in a separate window
    
       docTree=pq(text_response)
       #docTree=pq(response.content)
       #docTree.find('title').text()
       #docTree.find('p:eq(0)').text()
       #docTree.find('p:eq(2)').text()
    
       #[i.text() for i in docTree.items('p')] #iterates through all <p></p> tags
    
       art_sub_sections=[i.text() for i in docTree.items('p')] #creates a list of all text    sections of the article separated by commas
    
       #art1[0]+' '+art1[1] # constructs the first two subsections of the article as a string
    
       full_article=[] #create a location to store the full article (without being divided by <p> <\p> tags
    
       for w in range(len(art_sub_sections)):
          full_article = str(full_article) + ' ' + str(art_sub_sections[w])
       # now the full article is in full_article[0] as text
    
       article_text_putin.append(full_article)
       article_images_putin.append(img)
       # to show the article images use
       #article_images_putin[4].show()
       # to see the article text use
       # article_text_putin[4]
   
#end the loop
       
print('Length of valid article list for Putin is: ', len(article_text_putin))


"""
So we just need to iterate through the trump_list_links and collect full articles using the previous code

Then we need to collect the images and store them in a matrix with each record at the same index as the articles

Finally we need the title and seen date for each article and image respectively.

Put these altogether in a huge matrix with:
[{title, article, image, seen date}, {title, article, image, seen date}, ...]000
"""

# now lets write the variable datasets to a json file
import json
with open ('article_text_putin.json', 'w', encoding = 'utf-8') as f:
    json.dump(article_text_putin,f,ensure_ascii=False,indent=4)

with open ('article_text_trump.json', 'w', encoding = 'utf-8') as f:
    json.dump(article_text_trump,f,ensure_ascii=False,indent=4)
# we need to pickle the list of images because they are each a different size

import pickle
pickle.dump(article_images_trump, open( "article_images_trump.pkl", "wb") )
pickle.dump(article_images_putin, open( "article_images_putin.pkl", "wb") ) 




