# -*- coding: utf-8 -*-
import urllib2
from bs4 import BeautifulSoup
import sys, codecs,os
RAW_URL = "http://hansard.millbanksystems.com"
#years = xrange(1803,2006)
MONTHS = ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
DAYS = xrange(1,32)

def get_HANSARD_maintexts(years):
    for year in years:
        for month in MONTHS:
            for day in DAYS:
                try:
                    req = urllib2.urlopen(RAW_URL+"/sittings/"+str(year)+'/'+month+'/'+str(day))
                    soup = BeautifulSoup(req)
                    for span in soup.findAll('span',{"class":"major-section"}):
                        req2 = urllib2.urlopen(RAW_URL+span.find('a').get('href'))
                        soup2 = BeautifulSoup(req2,"html5lib")
                        # parser を"html5lib" に指定しないとなぜか途中で切れる
                        title_text = soup2.find('h1',{'class':'title'}).get_text()
                        main_text = soup2.find('div',{'id':'content'}).get_text()
                        with open('./HANSARD/'+str(year)+'_'+month+'_'+str(day)+'_'+title_text, 'w') as f:
                            f = codecs.lookup('utf_8')[-1](f)
                            print >> f , main_text
                        print >> sys.stderr, str(year)+'_'+month+'_'+str(day),'(',len(main_text),')'
                except:
                    pass
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print >> sys.stderr, "please use ./get_hansard.py from_year(1803) to_year(2006)"
        print >> sys.stderr, "get main text from \"http://hansard.millbanksystems.com\" to ./HANSARD/"        
    else:
        try:
            os.mkdir("HANSARD")
        except OSError:
            pass
        Parser = get_HANSARD_maintexts(xrange(int(sys.argv[1]),int(sys.argv[2])))

