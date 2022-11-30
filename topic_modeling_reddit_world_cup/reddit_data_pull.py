import os
import praw
import time
import datetime
#import requests


CLIENT_ID = os.getenv('CLIENT_ID')
SECRET_TOKEN = os.getenv('SECRET_TOKEN')
reddit_username = os.getenv('reddit_username')
reddit_pw = os.getenv('reddit_pw')

'''
data = {'grant_type': 'password',
        'username': reddit_username>,
        'password': reddit_pw}
headers = {'User-Agent': 'reader_bot'}

auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_TOKEN)
res = requests.post('http://127.0.0.1',
                    auth=auth, data=data, headers=headers)

TOKEN = res.json()['access_token']

headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}
requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)


#'https://127.0.0.1/authorize_callback',#'https://www.reddit.com/api/v1/access_token'
'''

reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=SECRET_TOKEN,
    password=reddit_pw,
    user_agent='reader_bot',
    username=reddit_username,
)

subreddit = reddit.subreddit("soccer")
    
submission_fields = ('created_utc', 'author', 'id', 'permalink', 'num_comments', 'score', 'selftext', 'stickied', 'title', 'upvote_ratio', 'url')
reply_fields = ('author', 'id', 'score', 'stickied', 'body')

subreddit = reddit.subreddit("worldcup")
submissions_list = []

for submission in subreddit.top(limit=500, time_filter='week'):
    submission_dict_complete = vars(submission)
    submission_dict = {field:submission_dict_complete[field] for field in submission_fields}
    if submission_dict['author'] != None:
        submission_dict['author'] = submission_dict['author'].name
    top_level_replies_list = []
    submission.comments.replace_more(limit=0)
    for top_level_reply in submission.comments:
        reply_dict_complete = vars(top_level_reply)
        reply_dict = {field:reply_dict_complete[field] for field in reply_fields}
        if reply_dict['author'] != None:
            reply_dict['author'] = reply_dict['author'].name
        top_level_replies_list.append(reply_dict)
    submission_dict['top_level_replies'] = top_level_replies_list
    submissions_list.append(submission_dict)

    
t = time.time()
d = datetime.datetime.fromtimestamp(t).strftime('%Y-%m-%d %H:%M:%S')
with open('reddit_worldcup_data_500_weekly' + d + '.json', 'w') as f:
    json.dump(submissions_list, f)
    
