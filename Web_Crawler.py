from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd
import csv
from webdriver_manager.chrome import ChromeDriverManager

with open('Output.csv', mode='w') as csv_file:
   fieldnames = ['serial_no','Name', 'Product/Services', 'Website', 'Address', 'Contact_info']
   writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
   writer.writeheader()

def getdata(url):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    
    # driver.maximize_window()
    driver.get(url)

    time.sleep(5)
    content = driver.page_source.encode('utf-8').strip()
    soup = BeautifulSoup(content,"html.parser")
    return soup

def getnextpage(url,soup):
    page=soup.find("li",{"class":"active"})
    print("")
    
    print(url+str(page.find_next_sibling("li").find('a')['href']))
serial_no=[]
Name = []
Product_services = []
Website = []
Address = []
Contact_info = []


def scrapdata(soup,serialN):
       for b in soup.find_all('div',{'class':'upl_left upl_left_img'}):
            serial_no.append(serialN)
            serialN+=1
            nm=b.find('h4').find('a')
            prod=b.find('p').find_next_sibling('p')
            addr=prod.find_next_sibling('p')
            contact=addr.find_next_sibling('p')
            temp_url="Not Available"
            Name.append(" ".join(nm.text.split()))
            Product_services.append(" ".join(prod.text.split())[19:])
            Address.append(" ".join(addr.text.split())[8:])
            ci=" ".join(contact.text.split())
            if(ci[-1]==','):
                sz=len(ci)
                ci=ci[0:sz-1]
            Contact_info.append(ci[12:])
            if(contact.find_next_sibling('p')!=None):
                temp_url=contact.find_next_sibling('p').find('a')['href']
                
            Website.append(temp_url)

url="https://www.msmemart.com/msme/listings/company-list/advertising-materials/90/1297/Supplier"
k=getdata(url)
scrapdata(k,1)

data = { 'serial_no':serial_no,'Name': Name,
'Product/Services':Product_services, 'Website':Website, 'Address':Address, 'Contact Info':Contact_info}
df = pd.DataFrame(data, columns = ['serial_no','Name','Product/Services','Website','Address','Contact Info'])
df.to_csv(r'Output.csv',index=False)
