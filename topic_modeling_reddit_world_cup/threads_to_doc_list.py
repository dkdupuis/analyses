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

def threads_to_doc_list(filename):
    data = load_data(filename)
    return parse_submissions(data)