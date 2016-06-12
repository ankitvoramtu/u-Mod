from __future__ import print_function,absolute_import
import sys
sys.dont_write_bytecode = True
import json

from sqlalchemy import create_engine
import sqlalchemy
import lib.string_cleaning as string_cleaning
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship,sessionmaker
from sqlalchemy import create_engine

import os
import logging
import nltk
import string



#package imports
from config import DB_NAME, UNAME, PASSWORD
from create_db import Post,Comment,BASE, Author,CommentTree
import lib.liwk as liwk


def commit_or_rollback(session):
  print("commiting !")
  try :
    session.commit()
  except :
    session.rollback()

def merge_json(*args):
    j_return = {}
    for a in (args):
        j_return = dict(j_return.items()+a.items())
    return j_return


COMMIT_EVERY = 50000


bots = set(["reginaldtato","NotTheOnionBot","rSGSpolice","hwsbot","AutoModerator","yes_it_is_weird","r_PictureGame","prairiechicken2","domoarigatobtfcboto","SkydivingHaylz","I_Like_Spaghetti","STEALTHM0UNTAIN","Google_Panda","AakashMasani","Forestl","lurkattwork","drgoku282","texasmommie","Really_Like_Pancakes","BlaineWolfe","Blassie098","ghort98765","GustavoFrings","WritingPromptsRobot","sontato","ramsesniblick3rd","300BlackoutSober","flair_your_post_bot","GoomyTooOP","arbutus_","foamed","DumbCollegeStudent","[deleted]","GOTradeRuleBot","ShadowBanCheckBot","ShadowBannedBot","TrollaBot","Shiny_Sylveon","PaidBot","xbamsod","enriquepaz13","Moskau50","PornOverlord"])

engine = create_engine('postgresql://%s:%s@localhost/%s'%(UNAME,PASSWORD,DB_NAME))
DBSession = sessionmaker(bind=engine,expire_on_commit=False)



def add_posts_from_file(file):

  liwk_sentiment = liwk.liwk()
  #build posts
  session=DBSession()
  counter = 0
  with open(file) as f:
    for line in f:
      record = json.loads(line)
      if record['author'] not in bots:
        selftext_liwk = {}
        if record['selftext'] != '':
          record['selftext'] = string_cleaning.remove_stop_words(record['selftext'])

          #textblob sentiment(rough)
          selftext_sentiment = string_cleaning.get_sentiment(record['selftext'])
          record['selftext_polarity'] = selftext_sentiment.polarity
          record['selftext_subjectivity'] = selftext_sentiment.subjectivity

          #liwk sentiment(finer)
          selftext_liwk = json.loads(liwk_sentiment.sentiment(record['selftext'] , prefix = 'selftext_'))

        record['title'] = string_cleaning.remove_stop_words(record['title'])

        #textblob sentiment (rough)
        title_sentiment = string_cleaning.get_sentiment(record['title'])
        record['title_polarity'] = title_sentiment.polarity
        record['title_subjectivity'] = title_sentiment.subjectivity

        #liwk sentiment (finer)
        title_liwk=json.loads(liwk_sentiment.sentiment(record['title'], prefix = 'title_') )

        #smoosh together
        record = merge_json(title_liwk, selftext_liwk,record)

        post = Post(**record)
        session.add(post)
      counter += 1
      if counter == COMMIT_EVERY:
        commit_or_rollback(session)
        counter = 0
  commit_or_rollback(session)
  session.close()



#build comments
def add_comments_from_file(file):
  liwk_sentiment = liwk.liwk()
  session=DBSession()
  counter = 0
  with open(file)as f:
    for line in f:
      record = json.loads(line)
      record['body'] = string_cleaning.remove_stop_words(record['body'])

      #Text Blob Sentiment course
      record_sentiment = string_cleaning.get_sentiment(record['body'])
      record['body_polarity'] = record_sentiment.polarity
      record['body_subjectivity'] = record_sentiment.subjectivity

      #liwks sentiment fine gran
      title_liwk=json.loads(liwk_sentiment.sentiment(record['body'], prefix = "body_"))

      record = merge_json(record,title_liwk)

      comment = Comment(**record)
      session.add(comment)
      counter += 1
      if counter == COMMIT_EVERY:
        commit_or_rollback(session)
        counter = 0
  commit_or_rollback(session)
  session.close()


def main():
  # add_posts_from_file('/home/dstorey/Desktop/modU/data/political_data/three_month/01-02_political_posts.json')
  add_comments_from_file('/home/dstorey/Desktop/modU/data/political_data/three_month/01-02_political_comments.json')


if __name__ == '__main__':
  main()
