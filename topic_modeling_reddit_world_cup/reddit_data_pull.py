import os
import praw
import time
import datetime
import json

CLIENT_ID = os.getenv('CLIENT_ID')
SECRET_TOKEN = os.getenv('SECRET_TOKEN')
reddit_username = os.getenv('reddit_username')
reddit_pw = os.getenv('reddit_pw')

#pull_reddit_data(earliest_utc=1668988801, time_filter='month', submissions_to_query=5, submissions_to_save=3)
#pull_reddit_data(time_filter='month')

def pull_reddit_data(subreddit_name='worldcup', submissions_to_query=500, submissions_to_save=500, earliest_utc=None, time_filter='week'):
    
    reddit = praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=SECRET_TOKEN,
        password=reddit_pw,
        user_agent='reader_bot',
        username=reddit_username,
    )
    subreddit = reddit.subreddit(subreddit_name)
    
    submission_fields = ('created_utc', 'author', 'id', 'permalink', 'num_comments', 'score', 'selftext', 'stickied', 'title', 'upvote_ratio', 'url')
    reply_fields = ('author', 'id', 'score', 'stickied', 'body', 'created_utc')
    
    submissions_list = []
    num_submissions = 0
    
    for submission in subreddit.top(limit=submissions_to_query, time_filter=time_filter):
        submission_dict_complete = vars(submission)
        if num_submissions < submissions_to_save and (earliest_utc == None or submission_dict_complete.get('created_utc', -1) > earliest_utc):
            num_submissions = num_submissions + 1
            print(num_submissions)
            submission_dict = {field:submission_dict_complete[field] for field in submission_fields}
            if submission_dict['author'] != None:
                submission_dict['author'] = submission_dict['author'].name
            comments_list = []
            submission.comments.replace_more(limit=None)
            for comment in submission.comments.list():
                reply_dict_complete = vars(comment)
                reply_dict = {field:reply_dict_complete[field] for field in reply_fields}
                if reply_dict['author'] != None:
                    reply_dict['author'] = reply_dict['author'].name
                comments_list.append(reply_dict)
            submission_dict['comment_list'] = comments_list
            submissions_list.append(submission_dict)
    
    t = time.time()
    d = datetime.datetime.fromtimestamp(t).strftime('%Y-%m-%d %H:%M:%S')
    with open('reddit_' + subreddit_name + "_" + str(submissions_to_save) + "_" + d + '.json', 'w') as f:
        json.dump(submissions_list, f)

