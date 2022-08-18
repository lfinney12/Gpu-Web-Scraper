#Author: Levi Finney 
#Date: 8/17/22
#Description: Program utilizes BS4 to scrape data from websites. 
#The program ask the user what gpu they are looking for and spits out links on where to buy one 
#The cheapest ones are on the top of the list. The Website being scraped is Newegg 

from bs4 import BeautifulSoup
import requests 
import re

gpu = input("What graphics card do you want? ") 


#Newegg 
url = f'https://www.newegg.com/p/pl?d={gpu}&N=4131' #Will allow me to search for any gpu (Newegg Weibsite) 



page = requests.get(url).text 

doc = BeautifulSoup(page, 'html.parser') 


#Wanting to look through every page, 12 total

page_text = doc.find(class_ ='list-tool-pagination-text').strong #Need strong at the end because that's the tag that page number is in 



#Total number of pages of product listing for each individual graphics card
pages = int(str(page_text).split("/")[-2 ].split(">")[-1][:-1]) 


products_found = {} #using dict for how I want to print data 

for page in range(1, pages + 1): 
   url = f'https://www.newegg.com/p/pl?d={gpu}&N=4131&page={page}'
   page = requests.get(url).text
   doc = BeautifulSoup(page, 'html.parser') 
    # Only wanting what's inside of div
   div = doc.find(class_="item-cells-wrap border-cells items-grid-view four-cells expulsion-one-cell" )# Class was extracted from html of website 
   items = div.find_all(text = re.compile(gpu)) #Custom search filter 
   
   for item in items: 
       parent = item.parent
       if parent.name != 'a': #always making sure the parent is a tag 
           continue
      
       link = parent['href'] 
       next_parent = item.find_parent(class_ = 'item-container') 
       #Implemented a try and except block since some prices within the htlm body are present
       try: 
        price = next_parent.find(class_ ='price-current').find("strong").string #prices are in string tag 
        products_found[item] = {'price': int(price.replace(',','')), 'link': link} 
        #print(price)
       except: 
         pass


sorted_products = sorted(products_found.items(), key=lambda x: x[1]['price'])

#Prints products from least expensive to most expensive
for item in sorted_products: 
    print(item[0]) 
    print(f"${item[1]['price']}")
    print(item[1]['link']) 
   
    print('------------------------------------------------')
