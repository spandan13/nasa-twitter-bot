import tweepy
from nasaapi import Client
import nasapy
import json

#loonathedorm
# twt_api_key = 'csYcOAoLiUHLtCCANf2Utg94L'
# twt_secret_key = '6VkdKZ2ABhp8mU5OwFyHXsFqUuHBz3Kg2JgJQ70yRlst03KVPX'
# twt_token = '1575528129111547904-TUwvnV1fDoJlLhp5UyXuYckQpB6cK2'
# twt_secret_token = 'eTOnOi1WYwt36BOUBeUilOouKmzLLor163eFRz6dNnbPG'
# twt_bearer_token = 'AAAAAAAAAAAAAAAAAAAAANuYhgEAAAAAA9%2B732vxn0UueqK%2FZV5NHnn3GUA%3DhNkWpN6pVttSA2HpnTSITalAL08RI3R9F1ubhVowsYXMnVbJ8a'
# client_id = 'UmdBRDJ1TFFYLWhOYk1RVFhGaHA6MTpjaQ'
# client_secret = 'Em-dFljxdekc166pWASZi9qRGF1g3pY2lZ_x9l2iccbw7bZADT'
nasa_api_key = '4Ih5vtupnli8qtBxjKOcSCqsQZWVJRwMb79rgiTu'



twt_api_key = 'l7JgboDyIkYnApcUIzkmSQYP7'
twt_secret_key = 'cvw6kwhIB1XQnOTYOgKtdVDNYwPDPjWjBTuw7eqOTmvnZ2fP2l'
twt_token = '1575528129111547904-TUwvnV1fDoJlLhp5UyXuYckQpB6cK2'
twt_secret_token = 'eTOnOi1WYwt36BOUBeUilOouKmzLLor163eFRz6dNnbPG'
twt_bearer_token = 'AAAAAAAAAAAAAAAAAAAAAL%2BVhgEAAAAA%2F2%2FYY8LHeF%2B3%2B9YJ4AQr9KedX0Q%3DkxwjBK8hQa1M2QHpEeBkMarEW5ytf59Wd0pzRIE177V0UBShYn'
client = tweepy.Client(
    bearer_token=twt_bearer_token,
    consumer_key=twt_api_key,
    consumer_secret=twt_secret_key,
    access_token=twt_token,
    access_token_secret=twt_secret_token
)

auth = tweepy.OAuthHandler(twt_api_key, twt_secret_key)
auth.set_access_token(twt_token, twt_secret_token)
api = tweepy.API(auth)

nasa = nasapy.Nasa(key=nasa_api_key)

data = nasa.media_search(query='moon')
print(data)

# data = (nasa.nivl.search(query=''))
# print(data)

# text = "#loona @loonatheworld"
# tweets = []
# for tweet in api.search_tweets(q=text, result_type='recent', count=1, include_entities=False):
#     tweets.append(tweet)

# print(tweets)
