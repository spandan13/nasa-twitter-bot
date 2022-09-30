import datetime
"""This includes all functions used to log tweet posts and deletions"""

def log_line(post_number, tweet_id, media, reply_id, request_user):
    """Returns a string fit for the log from a post_number, tweet_id,
    img_path and reply_id.
    """
    date = str(datetime.datetime.now())
    log_line = post_number + '\t'
    log_line += str(tweet_id) + '\t'
    log_line += date + '\t'
    log_line += media + '\t'
    log_line += '@' + str(request_user) + '\t'
    log_line += str(reply_id) + '\n'
    return log_line

def add_line_to_log(line, log_file):
    """Appends line to the log_file."""
    with open(log_file, 'a') as log:
        log.write(line)
        
def add_banned_to_log(post_number, reply_id, log_file):
    """Appends a banned message to the log_file from a post_number, reply_id"""
    ban_message = "AN IMAGE WAS BANNED!"
    date = str(datetime.datetime.now())
    log_ban_line = (post_number + '\t' + date + '\t' + ban_message + '\t' + str(reply_id) + '\n')
    add_line_to_log(log_ban_line, log_file)
