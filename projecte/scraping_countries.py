# -*- coding: utf-8 -*-
#Llibreries del projecte
import csv
import datetime
import os
from bs4 import BeautifulSoup
import urllib3 as urllib
import urllib2

#Codificacio del text a emmagatzemar a disc
CODING = 'utf-8'

#Missatges
INIT_DOWNLOAD_LIST = 'Downloading url: '
ERROR_DOWNLOAD = 'Download error: '
FINISH_SCRAPING_PROJECT = 'Finish scraping project in: '
TIME = ' seconds'
ERROR_EMPTY_HTML = 'Error empty html for '
INIT_SCRAPING_LIST = 'Init scraping countries list'
FINISH_SCRAPING_LIST = 'Finish scraping countries list \n'
INIT_SCRAPING_DETAIL = 'Init scraping countries details'
MSG_TEMP = 'Please, be patient. The download can take a while'
FINISH_SCRAPING_DETAIL = 'Finish scraping countries details \n'

#Nom dels fitxers i extensio
COUNTRIES_LIST = 'countries_list.csv'
COUNTRIES_DETAIL = 'countries_details.csv'

#Web inicial i columnes a obtenir
BASE_URL = 'https://en.wikipedia.org'
COUNTRIES_EXT = '/wiki/List_of_sovereign_states_and_dependent_territories_by_continent'
ROWS_LIST = ["Link","Country","Capital","Status"]
ROWS_DETAIL = ["Country","Capital","Official language","Government",
               "Legislature","Gini","HDI","Currency","Time zone",
               "Drives on the","Calling code","ISO 3166 code","Internet TLD"]

#Funcio per a obtenir la web a tractar, extreta del llibre del curs
def download(url, num_retries=2):
    print INIT_DOWNLOAD_LIST, url
    try:
        html = urllib2.urlopen(url).read()
    except urllib2.URLError as e:
        print ERROR_DOWNLOAD, e.reason
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                # recursively retry 5xx HTTP errors
                return download(url, num_retries-1)
    return html

#Funcio que inicia l'scraping del projecte
def startScraping():
    urllib.disable_warnings()
    init = datetime.datetime.now()
    scrapingCountriesList(BASE_URL + COUNTRIES_EXT)
    end = datetime.datetime.now()
    print FINISH_SCRAPING_PROJECT, end-init, TIME

#Funcio per obtenir mitjançant scraping la llista dels paisos d'Africa
def scrapingCountriesList(url):
    listrows = []
    countriesurl = []
    countriesname = []

    html = download(url)

    if html == "":
        print(ERROR_EMPTY_HTML + url)
        return

    soup = BeautifulSoup(html, "lxml")

    tablelist = soup.find('table', class_='wikitable sortable')
    trs = tablelist.find_all('tr')

    listrows.append(ROWS_LIST)

    print INIT_SCRAPING_LIST

    for tr in trs:
        row = []
        for td in tr.find_all('td'):
            if (len(row) == 0):
                row.append(BASE_URL + td.a['href'])
                countriesurl.append(BASE_URL + td.a['href'])
                i = 1
            else:
                 row.append(td.text.encode(CODING))
                 if(i):
                     countriesname.append(td.text.encode(CODING))
                     i = 0

        listrows.append(row)

    writeCsvFile(COUNTRIES_LIST, listrows)
    print FINISH_SCRAPING_LIST
    scrapingCountriesDetail(countriesurl, countriesname)

#Funcio per obtenir mitjançant scraping la llista dels paisos d'Africa
def scrapingCountriesDetail(countries, names):
    detailrows = []
    
    print INIT_SCRAPING_DETAIL
    print MSG_TEMP

    detailrows.append(ROWS_DETAIL)

    for x in range(0,len(countries)):
        row = []
        url = countries[x]
        html = download(url)

        if html == "":
            print(ERROR_EMPTY_HTML + url)
            return

        soup = BeautifulSoup(html, "lxml")

        tablelist = soup.find('table', attrs={'class':'infobox geography vcard'})
        trs = tablelist.find_all('tr')       

        i = 1
        
        row.append(names[x])

        for tr in trs:
            th = tr.find('th', attrs={'scope':'row'})

            if (th != None):

                t = (" ".join(th.text.split())).lower()

                trobat = getDetail(t, i, row)

                if(trobat > 0):
                    td = tr.find('td')
                    row.append(td.text.encode(CODING))
                    i += trobat

        detailrows.append(row)
            
    writeCsvFile(COUNTRIES_DETAIL, detailrows)
    print FINISH_SCRAPING_DETAIL

#Funcio per obtenir la informacio detallada dels paisos
def getDetail(t, i, row):

    for k in range(i,len(ROWS_DETAIL)):
        d = (" ".join(ROWS_DETAIL[k].split())).lower()
        if(d in t):
            if(k > i):
                blankMissingInfo(k - i, row)
            #return k 
            return (k - i + 1)
    return 0
            
#Funcio que fica blancs en la informacio faltant
def blankMissingInfo(blank, row):
    m = 0

    for j in range(m,blank):
        row.append(" ")

#Funcio per escriure fitxers en format csv
def writeCsvFile(filename, rows):
    
    csvoutput = csv.writer(open(filename, 'w'))
    csvoutput.writerows(rows)

#Inici del projecte
startScraping()
