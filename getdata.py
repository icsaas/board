#-*- coding:utf-8 -*-
from pyquery import PyQuery as pq
import datetime
from main import _execute
url='http://tianchi.aliyun.com/competition/rankingList.htm?spm=0.0.0.0.cd6p0g&season=0&raceId=1&pageIndex=%s'
# d=pq(url%1)
today=datetime.date.today()
for i in range(1,26):
    d=pq(url%i)
    links=d('.list-item')
    for item in links:
        rank =int(links(item).find('.ranking p').text().encode('utf-8').split()[0])
        members = links(item).find('.member .member-box p').text().encode('utf-8')
        team = links(item).find('.team .team-box p').text().encode('utf-8')
        score = links(item).find('.score').text().encode('utf-8')
        accuracy =  links(item).find('.rate-accuracy').text().encode('utf-8')
        recall = links(item).find('.rate-recall').text().encode('utf-8')
        besttime=datetime.datetime.strptime(links(item).find('.best-time').text(),'%Y-%m-%d').date()
        _execute("""insert into rank (rank,members,team,score,accuracy,recall,besttime,currdate) values
           ("{0}","{1}","{2}","{3}","{4}","{5}","{6}","{7}");""".format(rank,members,team,score,accuracy,recall,besttime,today))
