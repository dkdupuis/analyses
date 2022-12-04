import json

def load_data(filename):
    with open(filename,"r") as f:
        d = json.load(f)
    return d

def parse_submissions(data):
    doc_list = []
    for submission in data:
        submission_texts = submission.get('title', '') + ' ' + submission.get('selftext', '') + ' '
        for reply in submission.get('top_level_replies', []):
            submission_texts = submission_texts + reply.get('body', '') + ' '
        doc_list.append(submission_texts)
    return doc_list

def num_words(text):
    return len(text.split(' '))

def parse_submissions_exploded(data, latest_time=None):
    doc_list = []
    for submission in data:
        if latest_time is None or submission.get('created_utc', 0) <= latest_time:
            if num_words(submission.get('title', '')) >= 5:
                doc = {'text':submission.get('title', ''), 'created_utc':submission.get('created_utc', 0)}
                doc_list.append(doc)
            reply_list = submission.get('top_level_replies', []) + submission.get('replies', [])
            for reply in reply_list:
                if num_words(reply.get('body', '')) >= 5:
                    doc = {'text':reply.get('body', ''), 'created_utc':reply.get('created_utc', 0)}
                    doc_list.append(doc)
    return doc_list

def threads_to_doc_list(filename):
    data = load_data(filename)
    return parse_submissions(data)

def threads_to_exploded_doc_list(filename, latest_time=None):
    data = load_data(filename)
    return parse_submissions_exploded(data, latest_time)