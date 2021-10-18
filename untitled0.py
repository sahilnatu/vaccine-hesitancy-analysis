# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 11:00:57 2021

@author: sahil
"""

import tweepy
import pandas as pd
import nltk
import numpy as np
import matplotlib as plt
import math
from sklearn.manifold import MDS



keys = pd.read_csv(r'C:\Users\sahil\Google Drive\UT Austin\College\Fall\Unstructured\Project\twitter_keys.csv')
keys.set_index('type',inplace=True)

#auth = tweepy.OAuthHandler(keys.loc['consumer','key'], keys.loc['consumer','secret'])
auth = tweepy.AppAuthHandler(keys.loc['consumer','key'], keys.loc['consumer','secret'])
#auth.set_access_token(keys.loc['access','key'], keys.loc['access','secret'])

api = tweepy.API(auth, wait_on_rate_limit=True)


result_df = pd.DataFrame(columns=('user_id','user','tweet_id','text','location','date'))
#followed_users_list = []
total = 0
max_id=0
users = ['@FoxNews','@newsmax','@planetInfowars','@DailyCaller','@TuckerCarlson','@benshapiro','@CNN','@ABC','@WHO','@CDCgov']
for i in range(len(users)):
    total=0
    print('total is reset')
    while total<5000:
        print('inside while')
        if total==0:
            count = 0
            for tweet in api.search_tweets(q="{0} covid".format(users[i]), lang="en", count=100):
                place = None
                if tweet.place!=None:
                    place = str(tweet.place).split("', ")[4].split("='")[1]
                result_df = result_df.append(pd.DataFrame([[tweet.user.id, tweet.user.screen_name, tweet.id, tweet.text, place, tweet.created_at]],columns=('user_id','user','tweet_id','text','location','date')),ignore_index=True)
                total = total+1
                count = count+1
                print(total)
            if count < 2:
                total = 5000
            else:
                max_id = result_df.iloc[-1,2]
        else:
            count = 0
            for tweet in api.search_tweets(q="{0} covid".format(users[i]), lang="en", max_id=max_id, count=100):
                place = None
                if tweet.place!=None:
                    place = str(tweet.place).split("', ")[4].split("='")[1]
                result_df = result_df.append(pd.DataFrame([[tweet.user.id, tweet.user.screen_name, tweet.id, tweet.text, place, tweet.created_at]],columns=('user_id','user','tweet_id','text','location','date')),ignore_index=True)
                total = total+1
                count = count+1
                print(total)
            if count < 2:
                total = 5000
            else:
                max_id = result_df.iloc[-1,2]
            
result_df.to_csv(r'C:\Users\sahil\Google Drive\UT Austin\College\Fall\Unstructured\Project\mentions_tweets.csv', index = False, header=True)


#users = ['@FoxNews','@newsmax','@planetInfowars','@DailyCaller','@TuckerCarlson','@benshapiro','@CNN','@ABC','@WHO','@CDCgov']
#users = ['@naa_two']
#result_df_2 = pd.DataFrame(columns=('user','id','text','created_at'))
#total = 0
#max_id= ['']*len(users)
#for i in range(len(users)):
#    print(users[i])
#    total = 0
#    while total<3000:
#        if total==0:
#            for tweet in api.user_timeline(screen_name=users[i], count=20, exclude_replies=False, include_rts=True):
#                result_df_2 = result_df_2.append(pd.DataFrame([[users[i],tweet.id, tweet.text, tweet.created_at]],columns=('user','id','text','created_at')),ignore_index=True)
#                total = total+1
#                print(total)
#            max_id[i] = str(result_df_2.iloc[-1,1])
#            print(max_id[i])
#        else:
#            for tweet in api.user_timeline(screen_name=users[i], count=20, exclude_replies=False, include_rts=True, max_id=max_id[i]):
#                result_df_2 = result_df_2.append(pd.DataFrame([[users[i],tweet.id, tweet.text, tweet.created_at]],columns=('user','id','text','created_at')),ignore_index=True)
#                total = total+1
#                print(total)
#            max_id[i] = str(result_df_2.iloc[-1,1])
#            print(max_id[i])
#            
#result_df_2.to_csv(r'C:\Users\sahil\Google Drive\UT Austin\College\Fall\Unstructured\Project\user_tweets.csv', index = False, header=True)
#max_id_df = pd.DataFrame(max_id)
#max_id_df.to_csv(r'C:\Users\sahil\Google Drive\UT Austin\College\Fall\Unstructured\Project\user_tweets_max_id.csv', index = False, header=True)