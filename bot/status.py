import os

"""Handles all statuses from the bot"""

class Tweet():
    def __init__(self, media, tweet_text, reply_id=None):
        self.text = tweet_text
        self.media = media
        self.reply_id = reply_id
        
    def post_to_twitter(self, api):
        try:
            status = api.update_status_with_media(filename=self.media, status=self.text, in_reply_to_status_id=self.reply_id)
            return status.id
        except Exception as err:
            print(f'Failed to post: {err} - Media={self.media} Tweet={self.reply_id}')
            raise
        
        
def delete_tweet_by_id(tweet_id, api):
    """Deletes the tweet mentioned"""
    api.destroy_status(tweet_id)