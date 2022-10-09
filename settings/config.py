import os
import configparser
import tweepy
import ast

"""Reads the settings file which holds all values and keys"""

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
config = configparser.ConfigParser()
config.read(dname + '/settings')

api_config = config['ApiKeys']
twt_api_key = api_config['twt_api_key']
twt_secret_key = api_config['twt_secret_key']
twt_token = api_config['twt_token']
twt_secret_token = api_config['twt_secret_token']
nasa_api_key = api_config['nasa_api_key']

app_config = config['App']
allow_repeat_after = int(app_config['allow_repeat_after'])
apod_time = app_config['apod_time']
log_file = app_config['log_file']
bot_account = app_config['bot_account']
master_account = app_config['master_account']
banned_twt = app_config['banned_twt']
blocked = app_config['blocked']
temp_downloads = app_config['temp_downloads']
search_terms = ast.literal_eval(app_config['search_terms'])

orders_config = config['Orders']
ban_command = orders_config['ban_command']
request_commands = orders_config['request_commands'].split('\n')
time_tolerance = float(orders_config['time_tolerance'])

text_config = config['Texts']
tweet_text = text_config['tweet_text']

#Twitter Api
auth = tweepy.OAuthHandler(twt_api_key, twt_secret_key)
auth.set_access_token(twt_token, twt_secret_token)
api = tweepy.API(auth)