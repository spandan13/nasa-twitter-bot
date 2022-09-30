from multiprocessing.connection import Client
import os
import configparser
import tweepy
import ast

"""Reads the settings file which holds all values and keys"""

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
config = configparser.configparser()
config.read(dname + '/settings')

api_config = config['ApiKeys']
twt_api_key = api_config['twt_api_key']
twt_secret_key = api_config['twt_secret_key']
twt_token = api_config['twt_token']
twt_secret_token = api_config['twt_secret_token']
twt_bearer_token = api_config['twt_bearer_token']
nasa_api_key = api_config['nasa_api_key']

app_config = config['App']
allow_repeat_after = app_config['allow_repeat_after']
log_file = app_config['log_file']
bot_account = app_config['bot_account']
master_account = app_config['master_account']
banned_twt = app_config['banned_twt']
blocked = app_config['blocked']
search_terms = ast.literal_eval(app_config['search_terms'])

orders_config = config['Orders']
ban_command = orders_config['ban_command']
request_commands = orders_config['request_commands'].split('\n')
time_tolerance = float(orders_config['time_tolerance'])

text_config = config['Texts']
tweet_text = text_config['tweet_text']
extra_text = text_config['extra_text']


#Nasa Api
nasa = Client(nasa_api_key)

#Twitter Api
auth = tweepy.OAuthHandler(twt_api_key, twt_secret_key)
auth.set_access_token(twt_token, twt_secret_token)
api = tweepy.API(auth)

"""
TwitterApi v2 Auth

client = tweepy.Client(
    bearer_token=twt_bearer_token,
    consumer_key=twt_api_key,
    consumer_secret=twt_secret_key,
    access_token=twt_token,
    access_token_secret=twt_secret_token
)
"""