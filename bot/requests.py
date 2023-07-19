import datetime
import re
import requests
import random


def get_nasa_img(query, temp_download, search_terms):
    """Pulls media, caption and details for
    random image from given query using NASA API"""
    try:
        url = (f'https://images-api.nasa.gov/search?media_type=image&q={query}')
        data = requests.get(url).json()['collection']['items']
        img = random.choice(data)['data'][0]
    except IndexError:
        query = random.choice(search_terms).replace(' ','%20')
        url = (f'https://images-api.nasa.gov/search?media_type=image&q={query}')
        data = requests.get(url).json()['collection']['items']
        img = random.choice(data)['data'][0]
    caption = img['title']
    img_id = img['nasa_id']
    details = "https://images.nasa.gov/details-" + img_id
    media_link = "https://images-assets.nasa.gov/image/" + img_id + '/' + img_id
    media = get_img_file(media_link, img_id, temp_download)
    return media, caption, details, query
    
def search_query(request_text, search_terms):
    """Determines serach query to be used for simple requests"""
    if '#' in request_text: #If query specified in request tweet
        query = (request_text.split('#')[1].split()[0]).replace('_', '%20')
    else: #If no query specified, choose random from settings
        query = random.choice(search_terms).replace(' ','%20')
    return query

def get_apod(api_key, date, temp_download):
    """Gets media, caption and details
    for APOD using NASA API"""
    apod_url = (f"https://api.nasa.gov/planetary/apod?api_key={api_key}&")
    apod = requests.get(f'{apod_url}date={date}').json()
    media_link = apod['url']
    if 'youtube' in media_link: #If APOD is a youtube video, post thumbnail
        media_link = (f"https://img.youtube.com/vi/{media_link.split('/')[-1].split('?')[0]}/maxresdefault.jpg")
    file_ext = media_link.split('.')[-1]
    caption = apod['title']
    details = (f"https://apod.nasa.gov/apod/ap{date[2:].replace('-','')}.html")
    media = get_img_file(media_link, date, temp_download, file_ext, apod=True)
    return media, caption, details

def apod_posted(log, date):
    """Checks if Daily APOD already posted"""
    with open(log,'r') as log_file:
        for line in log_file.readlines():
            if "@APOD" in line and line.split('\t')[2].split()[0] == date:
                return True
        else:
            return False

def get_img_file(media_link, id, temp, file_ext="jpg", apod=False, news=False):
    """Downloads media to temporary folder"""
    filename = (f'{temp}{id}.{file_ext}')
    if apod or news: # For apod requests
        request = requests.get(url=(media_link), stream=True)
        with open(filename, 'wb') as image:
            for chunk in request:
                image.write(chunk)
    else: # For normal requests
        request = requests.get(url=(media_link+'~large.jpg'), stream=True) #First tries to download 'large' quality
        if request.status_code == 200:
            with open(filename, 'wb') as image:
                for chunk in request:
                    image.write(chunk)
        else:
            request = requests.get(url=(media_link+'~orig.jpg'), stream=True) #If 'large' unavailable, download 'original'
            with open(filename, 'wb') as image:
                for chunk in request:
                    image.write(chunk)
    return filename

def mentions(bot_account, scrape):
    """Pulls recent mentions to the bot
        using the twitter api"""
    mentions = []
    search_text = (bot_account + ' ' + '-filter:retweets' + ' ' + '-from:' + bot_account)
    raw_data = scrape.run(
        limit=10,
        retries=1,
        queries=[
            {
                'category': 'Latest',
                'query': search_text
            }
        ]
    )
    for raw_tweet in raw_data[0]:
        tweet_details = raw_tweet['content']['itemContent']['tweet_results']['result']
        tweet_id = tweet_details['rest_id']
        user_id = tweet_details['core']['user_results']['result']['rest_id']
        user_name = tweet_details['core']['user_results']['result']['legacy']['screen_name']
        created_at = tweet_details['legacy']['created_at']
        full_text = tweet_details['legacy']['full_text']
        try:
            in_reply_to = tweet_details['legacy']['in_reply_to_status_id_str']
        except KeyError:
            in_reply_to = None
        tweet = {'tweet_id':tweet_id,'user_id':user_id,'user_name':user_name,'created_at':created_at,'full_text':full_text,'in_reply_to':in_reply_to}
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
    created_at = datetime.datetime.strptime(tweet['created_at'], "%a %b %d %H:%M:%S %z %Y")
    tweet_date = (created_at).replace(tzinfo=None)
    time_since_order = datetime.datetime.now() - tweet_date
    return time_since_order < expiration_time

def already_answered(tweet, log):
    """Return true if tweet id found in log"""
    with open(log, 'r') as log:
        for line in log:
            if str(tweet['tweet_id']) in line:
                return True
        else:
            return False

def is_img_request(tweet, bot_account, command):
    """Return True if mention start with the request_command."""
    str_mention = (" " + tweet['full_text'].lower() + " ")
    if re.search("\s" + command.lower() + "\S*\s+" + bot_account.lower() + "\s+.*?", str_mention):
        return True
    else:
        return False

def master_mentions(mentions, log, master):
    "All the mentions to the bot from the master account"
    master_mentions = []
    for tweet in mentions:
        if ('@' + tweet['user_name']).lower() == master and not already_answered(tweet, log):
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
    mention = tweet['full_text'].lower()
    ban_command = ban_command.lower()
    return ban_command in mention

def ban_image_by_tweet_id(tweet_id, banned_file, log_file):
    """Bans the image posted in tweet_id."""
    for line in reversed(list(open(log_file, 'r').readlines())):
        line = line.split()
        if line[1] == str(tweet_id):
            with open(banned_file, 'a') as banned_file:
                banned_file.write(line[4] + '\n')
            break