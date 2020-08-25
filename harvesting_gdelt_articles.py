# -*- coding: utf-8 -*-
"""
Spyder Editor
This code will pull 100 article urls from each quarter of Calendar Year 2020 for two political figures from the GDELT dataset. Then we pull the full article, it's title, it's image, and the image seen date and compile them into a large matrix for processing with AI/ML. 

"""
import urllib
import requests

names=["trump", "putin"]
articles_per_quarter=10

# establish content breadth
CY20Q1_trumplink ="https://api.gdeltproject.org/api/v2/doc/doc?query=imagewebtag:%22trump%22&mode=artlist&startdatetime=20200101000000&enddatetime=20200331235959&sourcelang:english&format=JSON&maxrecords=10"
CY20Q2_trumplink ="https://api.gdeltproject.org/api/v2/doc/doc?query=imagewebtag:%22trump%22&mode=artlist&startdatetime=20200401000001&enddatetime=20200630235959&sourcelang:english&format=JSON&maxrecords=10"
CY20Q3_trumplink ="https://api.gdeltproject.org/api/v2/doc/doc?query=imagewebtag:%22trump%22&mode=artlist&startdatetime=20200701000001&enddatetime=20200816000000&sourcelang:english&format=JSON&maxrecords=10"

CY20Q1_putinlink ="https://api.gdeltproject.org/api/v2/doc/doc?query=imagewebtag:%22putin%22&mode=artlist&startdatetime=20200101000000&enddatetime=20200331235959&sourcelang:english&format=JSON&maxrecords=10"
CY20Q2_putinlink ="https://api.gdeltproject.org/api/v2/doc/doc?query=imagewebtag:%22putin%22&mode=artlist&startdatetime=20200401000001&enddatetime=20200630235959&sourcelang:english&format=JSON&maxrecords=10"
CY20Q3_putinlink ="https://api.gdeltproject.org/api/v2/doc/doc?query=imagewebtag:%22putin%22&mode=artlist&startdatetime=20200701000001&enddatetime=20200816000000&sourcelang:english&format=JSON&maxrecords=10"


links_trump = [CY20Q1_trumplink, CY20Q2_trumplink, CY20Q3_trumplink]
links_putin = [CY20Q1_putinlink, CY20Q2_putinlink, CY20Q3_putinlink]

# define containers

#links = [CY20Q1_link]
article_list_trump=[]
article_text_trump=[]
artile_images_trump=[]

article_list_putin=[]
article_text_putin=[]
article_images_putin=[]

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
import urllib
from pyquery import PyQuery as pq
from lxml import etree


# response = urlopen('https://news.yahoo.com/residents-turned-arizona-purple-made-113109884.html').read() 

# need to start a loop here to go through the article_list_trump and putin
for i in range(len(article_list_trump)):

   response = urlopen(article_list_trump[0]['url']).read()

   docTree=pq(response)
   #docTree.find('title').text()
   #docTree.find('p:eq(0)').text()
   #docTree.find('p:eq(2)').text()

   [i.text() for i in docTree.items('p')] #iterates through all <p></p> tags

   art_sub_sections=[i.text() for i in docTree.items('p')] #creates a list of all text    sections of the article separated by commas

   #art1[0]+' '+art1[1] # constructs the first two subsections of the article as a string

   full_article=[] #create a location to store the full article (without being divided by <p> <\p> tags

   for i in range(len(art_sub_sections)):
      full_article[0] = str(full_article[0]) + ' ' + str(art_sub_sections[i])
# now the full article is in full_article[0] as text

   article_text_trump.append(full_article[0])

#end the loop

#write the result to a textfile
import numpy as np
np.savetxt('article_text_trump.txt', article_text_trump) 
"""
So we just need to iterate through the trump_list_links and collect full articles using the previous code

Then we need to collect the images and store them in a matrix with each record at the same index as the articles

Finally we need the title and seen date for each article and image respectively.

Put these altogether in a huge matrix with:
[{title, article, image, seen date}, {title, article, image, seen date}, ...]
"""
