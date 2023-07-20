import os
import tweepy

"""Handles all statuses from the bot"""

class Tweet():
    def __init__(self, media, tweet_text, reply_id=None):
        self.text = tweet_text
        self.media = media
        self.reply_id = reply_id
        
    def post_to_twitter(self, api, auth_v1):
        """Sends media and details to twitter"""
        try:
            api_v1 = tweepy.API(auth_v1)
            media = api_v1.media_upload(self.media)
            media_id = media.media_id
            if self.reply_id=="SELF TWEET": self.reply_id = None
            status = api.create_tweet(media_ids=[media_id], text=self.text, in_reply_to_tweet_id=self.reply_id)
            return status[0]["id"]
        except Exception as err:
            print(f'Failed to post: {err} - Media={self.media} Tweet={self.reply_id}')
            raise
        finally:
            os.remove(self.media)
