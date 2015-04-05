import urllib2
from pyquery import PyQuery as pq
import csv

def writeToCsv(jq,writer):
    table=jq('.tr3')
    for i in table:
        vol=pq(i).find('td.b').text()
        red=pq(i).find('td.cred').text().split()
        blue=pq(i).find('td.cblue').text().split()
        data=[int(vol)]
        for item in red:
            data.append(int(item))
        for item in blue:
            data.append(int(item))

        writer.writerow(data)
csvfile=file('datatou.csv','wb')
writer=csv.writer(csvfile)
writer.writerow(['期号','红1','红2','红3','红4','红5','蓝1','蓝2'])

url='http://www.sunlava.com/datetou_history.htm'
index=0

while(url):
    print index,url
    index+=1

    req=urllib2.Request(url)
    response=urllib2.urlopen(req)
    html=response.read()
    jq=pq(html)
    writeToCsv(jq,writer)
    url=jq('.page-next').attr('href')
    if url:
        url='http://www.sunlava.com/'+url

csvfile.close()
print 'done'

