import datetime
import re
from nasaapi import Client


def get_nasa_img(query, nasa):
    """Should return media, caption and post link"""
    pass

def search_query(request_text, search_terms):
    pass

def mentions(bot_account, api):
    """Pulls recent mentions to the bot
        using the twitter api"""
    mentions = []
    search_text = (bot_account + ' ' + '-filter:retweets' + ' ' + '-from:' + bot_account)
    for tweet in api.search_tweets(q=search_text, result_type='recent', count=5, include_entities=False):
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
    tweet_date = tweet.created_at
    time_since_order = datetime.datetime.utcnow() - tweet_date
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
    if re.search("\s" + command.lower() + "\S*\s+" + bot_account + "\s+.*?", str_mention):
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
            if user == str(line.split('---')[0]):
                return True


def is_delete_order(tweet, ban_command):
    """Returns true if request is a delete command"""
    mention = tweet.text.lower()
    ban_command = ban_command.lower()
    return mention.startswith(ban_command)