#-*- coding:utf-8 -*-
from sqlalchemy import  Column,create_engine
from sqlalchemy.types import Integer,Float,String,Date
from sqlalchemy.ext.declarative import  declarative_base
DBCON_STRING='sqlite:///data.db'
engine=create_engine(DBCON_STRING,echo=False,strategy='threadlocal')
BaseModel=declarative_base()

class Rank(BaseModel):
    __tablename__='rank'
    id=Column(Integer,primary_key=True,autoincrement=True)
    rank=Column(Integer)
    members=Column(String(100))
    team=Column(String(100))
    score=Column(String(30))
    accuracy=Column(String(30))
    recall=Column(String(30))
    besttime=Column(Date)
    currdate=Column(Date)

if __name__=="__main__":
    BaseModel.metadata.create_all(engine,checkfirst=True)
