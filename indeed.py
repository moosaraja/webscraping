#creation Date : 03/11/2021
#Details: Webscrap the indeed.de jobs for the database administrator from Linda 100KM
#Developed by : Moosa Raja
#learned from Youtube: 

from bs4.element import PageElement
import requests
from bs4 import BeautifulSoup
import pandas as pd

def extractDate(page):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'}
    url = 'https://de.indeed.com/Jobs?q=Ms%20SQL%20%2B%20Administrator&l=Lindau&radius=100&start={page}&vjk=4b42359852b18e17'
    r = requests.get(url,headers)
    soup = BeautifulSoup(r.content,'html.parser')
    return soup

def transformData(soup):
    #divsJobTitle = soup.find_all('div', class_='heading4 color-text-primary singleLineTitle tapItem-gutter')
    divsJobTitle = soup.find_all('table', class_='jobCard_mainContent')
    for item in divsJobTitle:
        JobTitle = item.find('span').text
        try:
            Company = item.find('span', class_ = 'companyName').text.strip()
            CompanyLocation = item.find('div', class_ = 'companyLocation').text.strip()
        except:
            Company = 'Company Name not found'
            CompanyLocation = 'Company Location not found'
        #print(CompanyLocation)
        job = {
            'JobTitle'          : JobTitle,
            'Company'           : Company,
            'CompanyLocation'   : CompanyLocation
        } 
        joblist.append(job)    
    
    
    divsJobSummary = soup.find_all('table', class_='jobCardShelfContainer')
    for item2 in divsJobSummary:
        jobDescription = item2.find('li').text.strip().replace('\n','')
        #print(jobDescription)
        job = {
            'JobDescription'          : jobDescription
        }
    
        joblist.append(job)
    
    return

joblist = []
for i in range(0,40,10):
    print(f'Getting page, {i}')
    Content = extractDate(0) #first Page
    #print(transformData(Content))
    transformData(Content)

df = pd.DataFrame(joblist)
print(df.head())
df.to_csv('jobs.csv')
#print(joblist)
