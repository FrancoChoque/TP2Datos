 #!/usr/bin/python3.6
import urllib2
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from random import choice
import requests
try:		    # Python 2
	from itertools import izip
except ImportError:
		    # Python 3
    izip = zip

from itertools import islice

desktop_agents = [
   #Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    #Firefox
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
]
proxies = [
	{"http":'http://190.15.195.64:47912',
	"https":'http://190.15.195.64:47912'},
	{"http":'http://190.16.179.24:34848',
	"https":'http://190.16.179.24:34848'},
	{"http":'http://181.167.238.28:60531',
	"https":'http://181.167.238.28:60531'},
	{"http":'http://186.56.99.103:56338',
	"https":'http://186.56.99.103:56338'},
	{"http":'http://200.81.169.242:52947',
	"https":'http://200.81.169.242:52947'},
	{"http":'http://181.47.8.154:42230',
	"https":'http://181.47.8.154:42230'}	
]
def random_headers():
    return {'User-Agent': choice(desktop_agents),'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}
 
def ok(self):
    """Returns True if :attr:`status_code` is less than 400.

    This attribute checks if the status code of the response is between
    400 and 600 to see if there was a client error or a server error. If
    the status code, is between 200 and 400, this will return True. This
    is **not** a check to see if the response code is ``200 OK``.
    """
    try:
        self.raise_for_status()
    except HTTPError:
        return False
    return True

import csv
lista_sku_precios = []
with open('lista_skus_comprados.csv') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		print()
		raw_html = requests.get('https://www.trocafone.com.ar/comprar/checkout?trocable='+str(row['2683']),headers=random_headers(),proxies=choice(proxies))
		while not ok(raw_html):
			raw_html = requests.get('https://www.trocafone.com.ar/comprar/checkout?trocable='+str(row['2683']),headers=random_headers(),proxies=choice(proxies))
		html = BeautifulSoup(raw_html.text,'html.parser')
   		price = html.findAll("span",{"class":'js-trocable-price-text'})
   	 	if(not price):
   	 		continue
    	lista_sku_precios.append([row['2683'],int(price[0].text)])

with open ('precios_sku.csv','wb') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerow(lista_sku_precios)