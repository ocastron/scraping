# -*- coding: utf-8 -*-
import csv
import datetime
import os
from bs4 import BeautifulSoup
import urllib3 as urllib
import urllib2

UTF8 = 'utf-8'

BASE_URL = 'https://en.wikipedia.org'
COUNTRIES_EXT = '/wiki/List_of_sovereign_states_and_dependent_territories_by_continent'
ROWS_LIST = ["Link","Country","Capital","Status"]
ROWS_DETAIL = ["Country","Capital","Official language",
               "Currency","Time zone","Drives on the","Calling code",
               "ISO 3166 code","Internet TLD"]

def download(url, num_retries=2):
    print 'Downloading:', url
    try:
        html = urllib2.urlopen(url).read()
    except urllib2.URLError as e:
        print 'Download error:', e.reason
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                # recursively retry 5xx HTTP errors
                return download(url, num_retries-1)
    return html

def startScraping():
    urllib.disable_warnings()

    scrapingCountriesList(BASE_URL + COUNTRIES_EXT)

    print('Success crypto currencies!!!')


def scrapingCountriesList(url):
    listrows = []
    countriesurl = []
    countriesname = []

    html = download(url)

    if html == "":
        print("Error empty html for " + url)
        return

    soup = BeautifulSoup(html, "lxml")

    tablelist = soup.find_all('table', class_='wikitable sortable')
    trs = tablelist.find_all('tr')

    #append_list_title(listrows)
    listrows.append(ROWS_LIST)

    print('Init scraping in url: ' + url)

    
    for tr in trs:
        row = []

        for td in tr.find_all('td'):
            if (len(row) == 0):
                row.append(BASE_URL + td.a['href'])
                countriesurl.append(BASE_URL + td.a['href'])
                i = 1
            else:
                 row.append(td.text.encode(UTF8))
                 if(i):
                     countriesname.append(td.text.encode(UTF8))
                     i = 0

        listrows.append(row)

    now = datetime.datetime.now()

    writeCsvFile('count.csv', listrows)
    print('Finish url: ' + url)
    scrapingCountriesDetail(countriesurl, countriesname)

'''
def scrapingCountriesDetail(countries, names):
    detailrows = []
    
    print ('start scraping countries details')

    detailrows.append(ROWS_DETAIL)

    for x in range(41,49):
#    for x in range(0,len(countries)):
        row = []
        url = countries[x]
        html = download(url)

        if html == "":
            print("Error empty html for " + url)
            return

        soup = BeautifulSoup(html, "lxml")

        tablelist = soup.find('table', attrs={'class':'infobox geography vcard'})
        trs = tablelist.find_all('tr')       

        i = 1
        if (names[x] in "Mayotte") or (names[x] in "Réunion"):
            continue
        
        row.append(names[x])

        for tr in trs:
            th = tr.find('th', attrs={'scope':'row'})

            if (th != None):

                k = (" ".join(ROWS_DETAIL[i].split())).lower()
                t = (" ".join(th.text.split())).lower()

                if(k in t):
                    td = tr.find('td')
                    row.append(td.text.encode(UTF8))
                    i += 1
        
        detailrows.append(row)
        print('Finish url details: ' + url)
            
    writeCsvFile('details.csv', detailrows)
    print('Finish details')
'''

def scrapingCountriesDetail(countries, names):
    detailrows = []
    
    print ('start scraping countries details')

    detailrows.append(ROWS_DETAIL)

    for x in range(0,len(countries)):
        row = []
        url = countries[x]
        html = download(url)

        if html == "":
            print("Error: empty html for " + url)
            return

        soup = BeautifulSoup(html, "lxml")

        tablelist = soup.find('table', attrs={'class':'infobox geography vcard'})
        trs = tablelist.find_all('tr')       

        i = 1
        
        row.append(names[x])

        for tr in trs:
            th = tr.find('th', attrs={'scope':'row'})

            if (th != None):

#                k = (" ".join(ROWS_DETAIL[i].split())).lower()
                t = (" ".join(th.text.split())).lower()

                trobat = getDetail(t, i, row)

                if(trobat > 0):
                    td = tr.find('td')
                    row.append(td.text.encode(UTF8))
                    i += trobat

        detailrows.append(row)
        print('Finish url details: ' + url)
            
    writeCsvFile('details.csv', detailrows)
    print('Finish details')


def getDetail(t, i, row):

    for k in range(i,len(ROWS_DETAIL)):
        d = (" ".join(ROWS_DETAIL[k].split())).lower()

        if(d in t):
            if(k > i):
                blankMissingInfo(k - i, row)
            #return k 
            return (k - i + 1)
    return 0
            


def blankMissingInfo(blank, row):
    m = 0

    for j in range(m,blank):
        row.append(" ")

def appendDetailTitle(rows):
    rows.append( ["Country","Capital","Official Languages","Area",
                  "Population","Currency","Timezone",
                  "Drives on the","Calling code",
                  "ISO 3166 code","Internet LTD"])

        

def writeCsvFile(filename, rows):
    
    csvoutput = csv.writer(open(filename, 'w'))
    csvoutput.writerows(rows)

startScraping()
