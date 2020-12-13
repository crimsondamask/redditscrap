from dotenv import load_dotenv
import os, urllib.request, sys, praw, json, datetime

load_dotenv()
reddit = praw.Reddit(
        client_id=os.getenv('CLIENT_ID'),
        client_secret=os.getenv('CLIENT_SECRET'), 
        password=os.getenv('PASSWORD'),
        user_agent=os.getenv('USER_AGENT'), 
        username=os.getenv('REDDIT_USER')
        )
SUB = sys.argv[1]
if sys.argv[2] == "--limit" or sys.argv[2] =="-l":
    LIMIT = int(sys.argv[3])
    print("Will look for the top {} posts in the sub {}.".format(LIMIT, SUB))
else:
    LIMIT = 10

link_list = reddit.subreddit(SUB).top("all", limit=LIMIT)

def download(list):
    os.makedirs("/home/{}/Downloads/reddit/{}".format(os.getenv("USER"), SUB), exist_ok=True)
    for submission in link_list:
        filename = submission.created_utc
        url = submission.url
        ext = url.split('/')[-1].split('.')[-1]
        if ext == 'jpg' or ext == 'gif':
            metadata = {
                    'id': str(submission.id), 
                    'author': str(submission.author),
                    'date_created': str(datetime.datetime.fromtimestamp(submission.created_utc)), 
                    'title': str(submission.title)
                    }
            with open("/home/{}/Downloads/reddit/{}/{}.json".format(os.getenv("USER"), SUB, filename), 'w') as js:
                json.dump(metadata, js)
            print("Downloading post =====> {} ======>{}".format(submission.name, url))
            try:
                urllib.request.urlretrieve(url,
                        "/home/{}/Downloads/reddit/{}/{}.{}".format(os.getenv("USER"), SUB, filename, ext)
                        )
            except:
                pass
download(link_list)
