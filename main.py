#-*- coding:utf-8 -*-
import concurrent.futures
import MySQLdb
import markdown
import os.path
import re
import subprocess
import torndb
import tornado.escape
from tornado import gen
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import unicodedata
from tornado.options import define, options
from collections import namedtuple
from functools import partial
import datetime
from pandas_dbms import read_db
from pandas.io.sql import read_sql
import pandas as pd
define("port", default=8888, help="run on the given port", type=int)

import sqlite3
import json

def _execute(query):
    """Function to execute queries against a local sqlite database"""
    dbPath='data.db'
    connection=sqlite3.connect(dbPath)
    cursorobj=connection.cursor()
    try:
        cursorobj.execute(query)
        result=cursorobj.fetchall()
        connection.commit()
    except Exception:
        raise
    connection.close()
    return result


# A thread pool to be used for password hashing with bcrypt.
executor = concurrent.futures.ThreadPoolExecutor(2)

import uuid

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", ServiceHandler),
        ]
        settings = dict(
            blog_title=u"cbir.cc",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
            cookie_secret='bccbae44-62cc-4fc5-853b-0357c14dc400',
            login_url="/auth/login",
            debug=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)



class ServiceHandler(tornado.web.RequestHandler):
    """In tornado we need a class which is our service handler"""
    def get(self, *args, **kwargs):
        """Get HTTP verb which our service returns a list of rows from database"""
        # query="select * from rank where currdate='%s'" % datetime.date.today()
        # _execute(query)
        # with sqlite3.connect('data.db', detect_types=sqlite3.PARSE_DECLTYPES) as conn:
        #     df_sqlite = read_sql(query, con=conn)
        self.render("index.html")

    @tornado.web.asynchronous
    def post(self, *args, **kwargs):
        currtoday=datetime.date.today()
        query="select * from rank where currdate='%s'" % currtoday
        def callback(future):
            self.write(future.result())
            self.finish()
        executor.submit(partial(self.chartshandler,query)
        ).add_done_callback(lambda future: tornado.ioloop.IOLoop.instance().add_callback(partial(callback, future)))

    def chartshandler(self,query):
        # select predictive symbols maybe
        return DataTablesServer(query=query).output_result()

class DataTablesServer:
    def __init__(self,query):
        self.query=query
        # self.condition = {"resultid": {"$regex": con}, "Date": date}
        # connection to your mongodb (see pymongo docs). this is defaulted to localhost
    def output_result(self):
        output = {}
        output['sPaginationType'] = 'fullnamers'
        output['bProcessing'] = 1
        output['bDestroy'] = 1
        output['bRetrieve'] = 1

        try:
            with sqlite3.connect('data.db', detect_types=sqlite3.PARSE_DECLTYPES) as conn:
                df_sqlite = read_sql(self.query, con=conn,parse_dates=True)
            df_sqlite=df_sqlite.drop(['currdate','id'],axis=1)
            df_sqlite.rename(columns={'rank': '排名', 'members': '参赛者',
                                      'team':'所在组织','score':'评分',
                                      'accuracy':'准确率','recall':'召回率',
                                      'besttime':'最好成绩提交日'},
                             inplace=True)
            df_sqlite['最好成绩提交日']=df_sqlite['最好成绩提交日'].apply(lambda x: x.strftime('%Y-%m-%d'))
            datalist=df_sqlite.T.to_dict().values()
            if len(datalist) == 0:
                return "no data"
            output['aaData'] = datalist
            output['iTotalRecords'] = str(len(datalist))
            output['iTotalDisplayRecords'] = str(len(datalist))
        except Exception, e:
            print e
            output['aaData'] = []
            output['iTotalRecords'] = 0
            output['iTotalDisplayRecords'] = 0
            output['sEcho'] = 1
        finally:
            return output

    def run_queries(self):
        pass

    def filtering(self):
        pass

    def paging(self):
        pass
    def detailhandler(self, projid, symbolid):
        pass

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port,address='127.0.0.1')
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()