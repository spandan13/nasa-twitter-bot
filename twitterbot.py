#!/usr/bin/python

from settings import config
from bot import status
from bot import requests
from logs import logger
import datetime
import os

"""The main module that connects all modules together"""

def tweet_poster(reply_id, request_text, request_user, search_query, apod=False):
    """This function retrives image using nasa api and sends it to tweet poster module"""

    log = config.log_file
    api = config.api
    post_number = get_post_number(log)
    search_terms = config.search_terms

    if apod == True: #For APOD requests
        media, caption, details_link = requests.get_apod(search_query, config.temp_downloads)
        tweet_text = (f"@{request_user} \U0001F30C{config.tweet_text} #Astronomy Picture of the Day for {search_query}: {caption}. #NASA #APOD\n\U000027A1 More Details: {details_link}")
    else: #For simple requests
        media, caption, details_link, search_query = requests.get_nasa_img(search_query, config.temp_downloads, search_terms)
        while check_if_tweeted(media, log) or is_banned(media):
            media, caption, details_link, search_query = requests.get_nasa_img(search_query, config.temp_downloads, search_terms)
        tweet_text = (f"@{request_user} \U0001F30C{config.tweet_text} {caption}. #{search_query.capitalize().replace(' ','').replace('%20','')} #Space #NASA\n\U000027A1 More Details: {details_link}")
    
    t = status.Tweet(media, tweet_text, reply_id)
    tweet_id = t.post_to_twitter(api, config.auth_v1) #Posts tweet using twitter API
    log_line = logger.log_line(post_number, tweet_id, media.split('/')[5], reply_id, request_user)
    logger.add_line(log_line, log)
    print(f"@{str(request_user)} | {str(request_text)} | {str(media.split('/')[5])} | {str(tweet_id)}") #Prints tweet details to screen. Comment if not needed

    
def check_if_tweeted(media, log):
    """Checks if media pulled was already tweeted
    based on tolerance value in settings"""

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
        if line.split('\t')[3] == media.split('/')[5]:
            return True
    return False

def is_banned(media):
    """Checks if pulled media is banned"""
    ban_file = config.banned_twt
    #If ban_file does not exist then return false
    if not os.path.isfile(ban_file):
        return False
    with open(ban_file, 'r') as banned:
        banned_img = banned.readlines()
    for line in banned_img:
        if media.split('/')[5] == line.split()[0]:
            return True
    return False

def get_post_number(log):
    """Gets post number using logfile if present or 1"""
    try:
        with open(log, 'r') as log:
            post_number = (log.readlines()[-1]).split()[0]
            return str(int(post_number) + 1)
    except (IndexError, ValueError):
        return "1"

def respond_to_request(request_tweet):
    """Gets information necessary to respond to simple requests.
    Sends it forward to tweet_poster function"""
    post_number = get_post_number(config.log_file)
    request_text = request_tweet['full_text'].lower()
    reply_id = request_tweet['tweet_id']
    user_name = request_tweet['user_name']
    search_query = requests.search_query(request_text, config.search_terms)
    if requests.blocked(user_name, config.blocked):
        tweet_id = "Ignored:Blocked" #This was done to get info in logfile
        media = "No media posted"
        log_line = logger.log_line(post_number, tweet_id, media, reply_id, user_name)
        logger.add_line(log_line, config.log_file)
        print("Ignored:Blocked | @" + str(user_name) + " | " + str(request_text)) #Prints details to screen. Comment if not needed.
    else:
        return tweet_poster(reply_id, request_text, user_name, search_query)
    
def respond_to_apod(request_tweet):
    """Gets information necessary to respond to APOD requests.
    Sends it forward to tweet_poster function"""
    post_number = get_post_number(config.log_file)
    request_text = request_tweet['full_text'].lower()
    reply_id = request_tweet['tweet_id']
    user_name = request_tweet['user_name']
    try:
        search_date = request_text.split('#')[1].split()[0] #Gets APOD date mentioned in tweet
    except IndexError:
        search_date = str(datetime.date.today())
    if requests.blocked(user_name, config.blocked):
        tweet_id = "Ignored:Blocked" #This was done to get info in logfile
        media = "No media posted"
        log_line = logger.log_line(post_number, tweet_id, media, reply_id, user_name)
        logger.add_line(log_line, config.log_file)
        print("Ignored:Blocked | @" + str(user_name) + " | " + str(request_text)) #Prints details to screen. Comment if not needed.
    else:
        return tweet_poster(reply_id, request_text, user_name, search_date, apod=True)
    
    
def orders():
    """Handles orders and requests given to bot"""
    log = config.log_file
    time = config.time_tolerance
    master = (config.master_account).lower()
    ban_command = config.ban_command
    post_number = get_post_number(log)
    mentions = requests.mentions(config.bot_account, config.scrape)
    master_mentions = requests.master_mentions(mentions, log, master)
    relevant_mentions = requests.relevant_mentions(mentions, log, time)

    for tweet in relevant_mentions:
        for command in config.request_commands:
            if requests.is_img_request(tweet, config.bot_account, command):
                if "apod" in tweet['full_text'].lower(): #Checks if it is APOD request
                    respond_to_apod(tweet)
                else:
                    respond_to_request(tweet) #Else it is simple request
    
    for tweet in master_mentions:
        if requests.is_delete_order(tweet, ban_command):
            id_to_delete = tweet['in_reply_to']
            requests.ban_image_by_tweet_id(id_to_delete, config.banned_twt, config.log_file)
            logger.add_banned_to_log(post_number, tweet['tweet_id'], config.log_file)
            print("IMAGE BANNED: " + str(tweet['tweet_id']))

def daily_apod():
    """Posts daily APOD at time set in settings"""
    force_apod = True
    time_now = datetime.datetime.now().strftime("%H:%M")
    date = datetime.date.today()
    log = config.log_file
    post_number = get_post_number(log)
    if time_now == config.apod_time and not requests.apod_posted(log, str(date)) or force_apod == True:
        media, caption, details = requests.get_apod(str(date), config.temp_downloads)
        tweet_text = (f"\U0001F30C #Astronomy Picture of the Day - {date.strftime('%B %d %Y')}: {caption}. #APOD #NASA\n\U000027A1 More Details: {details}")
        t = status.Tweet(media, tweet_text, reply_id=None)
        tweet_id = t.post_to_twitter(config.api, config.auth_v1)
        log_line = logger.log_line(post_number, tweet_id, media.split('/')[5], reply_id=None, request_user='APOD')
        logger.add_line(log_line, log)
        print(f"APOD Posted | {str(media.split('/')[5])} | {str(tweet_id)}")

def main():
    """Runs the entire program with all functions"""

    daily_apod() #First checks if it is time to post APOD
    
    orders() #Then checks for requests and posts replies

if __name__ == "__main__":
    main()