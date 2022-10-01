import datetime
import re
#from nasaapi import Client
import requests
import random
import os


def get_nasa_img(query, api_url, temp_download):
    """Should return media, caption and post link"""
    url = (api_url + '&q=' + query)
    data = requests.get(url).json()['collection']['items']
    img = random.choice(data)['data'][0]
    caption = img['title']
    img_id = img['nasa_id']
    details = "https://images.nasa.gov/details-" + img_id
    media_link = "https://images-assets.nasa.gov/image/" + img_id + '/' + img_id
    media = get_img_link(media_link, img_id, temp_download)
    
    return media, caption, details
    
def search_query(request_text, search_terms):
    if '#' in request_text:
        query = (request_text.split('#')[1].split()[0]).replace('_', '%20')
    else:
        query = random.choice(search_terms).replace(' ','%20')
    return query

def get_img_link(media_link, id, temp):
    filename = temp + id + '.jpg'
    request = requests.get(url=(media_link+'~large.jpg'), stream=True)
    if request.status_code == 200:
        with open(filename, 'wb') as image:
            for chunk in request:
                image.write(chunk)
    else:
        request = requests.get(url=(media_link+'~orig.jpg'), stream=True)
        with open(filename, 'wb') as image:
            for chunk in request:
                image.write(chunk)
    return filename

def mentions(bot_account, api):
    """Pulls recent mentions to the bot
        using the twitter api"""
    mentions = []
    search_text = (bot_account + ' ' + '-filter:retweets' + ' ' + '-from:' + bot_account)
    for tweet in api.search_tweets(q=search_text, result_type='recent', count=5, include_entities='false'):
        mentions.append(tweet)
    return mentions

def relevant_mentions(mentions, log, time):
    """Returns tweets that are not beyond time tolerance
    and not already answered"""
    relevant_mentions = []
    for tweet in mentions:
        if is_recent(tweet, time) and not already_answered(tweet, log):
            relevant_mentions.append(tweet)
    return relevant_mentions

def is_recent(tweet, time_in_minutes):
    """Return true if tweet is recent when compared
    to the time in minutes as per settings"""
    expiration_time = datetime.timedelta(minutes=time_in_minutes)
    tweet_date = (tweet.created_at).replace(tzinfo=None)
    time_since_order = datetime.datetime.now() - tweet_date
    return time_since_order < expiration_time

def already_answered(tweet, log):
    """Return true if tweet id found in log"""
    with open(log, 'r') as log:
        for line in log:
            if str(tweet.id) in line:
                return True
        else:
            return False

def is_img_request(tweet, bot_account, command):
    """Return True if mention start with the request_command."""
    str_mention = (" " + tweet.text.lower() + " ")
    if re.search("\s" + command.lower() + "\S*\s+" + bot_account.lower() + "\s+.*?", str_mention):
        return True
    else:
        return False

def master_mentions(mentions, log, master):
    "All the mentions to the bot from the master account"
    master_mentions = []
    for tweet in mentions:
        if ('@' + tweet.user.screen_name) == master and not already_answered(tweet, log):
            master_mentions.append(tweet)
    return master_mentions

def blocked(user_name, blocked_list):
    """Returns true if username in blocklist"""
    user = "@" + user_name
    with open(blocked_list, 'r') as blocked:
        for line in blocked:
            if user == str(line.split()[0]):
                return True


def is_delete_order(tweet, ban_command):
    """Returns true if request is a delete command"""
    mention = tweet.text.lower()
    ban_command = ban_command.lower()
    return ban_command in mention