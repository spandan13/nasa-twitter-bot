#!/usr/bin/python

from settings import config
from bot import status
from bot import requests
from bot import timeline
from logs import logger
from logs import banner
import random
import argparse
import sys
import os

"""The main module that connects all modules together"""

def tweet_poster(reply_id, request_text, request_user, search_query):
    """This function retrives image using nasa api and sends it to tweet poster modules"""

    log = config.log_file
    repeat_after = config.allow_repeat_after
    api = config.api
    nasa_api = config.nasa
    post_number = get_post_number(log)

    media, caption, details_link = requests.get_nasa_img(search_query, nasa_api, config.api_url, config.temp_downloads)
    check_if_tweeted(media)

    while check_if_tweeted(media) or is_banned(media):
        media, caption, details_link = requests.get_nasa_img(request_text)
        check_if_tweeted(media)
        
    tweet_text = config.tweet_text + caption + details_link
    t = status.Tweet(media, tweet_text, reply_id)
    tweet_id = t.post_to_twitter(api)
    log_line = logger.log_line(post_number, tweet_id, media, reply_id, request_user)
    logger.add_line(log_line, log)

    
def check_if_tweeted(media):
    """Checks if image pulled was already tweeted
    based on tolerance value in settings"""

    log = config.log_file
    repeat_after = config.allow_repeat_after
    readlineAmount = -1*(repeat_after)
    if not os.path.isfile(log):
        return False
    ##If log file does not exist then return false
    
    try:
        with open(log, 'r') as log:
            already_tweeted = log.readlines()[readlineAmount:]
    except IndexError:
        with open(log, 'r') as log:
            already_tweeted = log.readlines()
    for line in already_tweeted:
        if line.split('\t')[2] == media:
            return True
    return False

def is_banned(media):
    """To be finished"""
    return False

def get_post_number(log):
    try:
        with open(log, 'r') as log:
            post_number = (log.readlines()[-1]).split()[0]
            return str(int(post_number + 1))
    except (IndexError, ValueError):
        return "1"

def respond_to_request(request_tweet):
    """Parse necessary information from request tweet
    needed to post a reply to it"""
    post_number = get_post_number(config.log_file)
    request_text = request_tweet.text.lower()
    reply_id = request_tweet.id
    user_name = request_tweet.user.screen_name
    search_query = requests.search_query(request_text, config.search_terms)
    if requests.blocked(user_name, config.blocked):
        tweet_id = "Ignored:Blocked"
        media = "No media posted"
        log_line = logger.log_line(post_number, tweet_id, media, reply_id, user_name)
        logger.add_line(log_line, config.log_file)
        print("Ignored:Blocked | @" + str(user_name) + " | " + str(request_text))
    else:
        return tweet_poster(reply_id, request_text, user_name, search_query)
    
    
def orders():
    """Handles orders given to bot via replies"""
    log = config.log_file
    time = config.time_tolerance
    master = config.master_account
    ban_command = config.ban_command
    api = config.api
    post_number = get_post_number(log)
    mentions = requests.mentions(config.bot_account, config.api)
    master_mentions = requests.master_mentions(mentions, log, master)
    relevant_mentions = requests.relevant_mentions(mentions, log, time)

    for tweet in relevant_mentions:
        for command in config.request_commands:
            if requests.is_img_request(tweet, config.bot_account, command):
                respond_to_request(tweet)
    
    for tweet in master_mentions:
        if requests.is_delete_order(tweet, ban_command):
            id_to_delete = tweet.in_reply_to_status_id
            status.delete_tweet_by_id(tweet.in_reply_to_status_id)
            banner.ban_image_by_tweet_id(id_to_delete, config.banned_twt, config.log_file)
            logger.add_banned_to_log(post_number, tweet.id, config.log_file)
            
            
def main():
    """Runs the entire program with all functions"""

    orders()

    ##Daily tweet function to be added here later
    
if __name__ == "__main__":
    main()