#!/user/bin/python
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
LIMIT = int(sys.argv[3])
if sys.argv[2] == "-h":
    link_list = reddit.subreddit(SUB).hot(limit=LIMIT)
    print("Looking for the {} hot submissions in the subreddit r/{}.".format(LIMIT, SUB))
elif sys.argv[2] == "-t" and sys.argv[4]:
    #(--all) for all and (--month) for month...
    top = sys.argv[4].split('--')[-1]
    link_list = reddit.subreddit(SUB).top(str(top), limit=LIMIT)
    print("Looking for the top {} submissions in the last {} in the subreddit r/{}.".format(LIMIT, top, SUB))
else:
    link_list = reddit.subreddit(SUB).top("all", limit=LIMIT)
    print("Looking for the top {} submissions of all time in the subreddit r/{}.".format(LIMIT, SUB))

def progress(count, blockSize, totalSize):
    percent = int(count * blockSize / totalSize * 100)
    sys.stdout.write("Progress ====================> %d%%       \r" %percent)
    sys.stdout.flush()

def download(list):
    os.makedirs("/home/{}/Downloads/reddit/{}".format(os.getenv("USER"), SUB), exist_ok=True)
    submission_count = 0
    error_count = 0
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
            try:
                print("\nDownloading submission {}  ".format(submission.name))
                urllib.request.urlretrieve(url,
                        "/home/{}/Downloads/reddit/{}/{}.{}".format(os.getenv("USER"), SUB, filename, ext),
                        reporthook=progress
                        )
                submission_count += 1
            except:
                error_count += 1
                pass
    print("{} submissions have been downloaded and {} sumissions have been excluded.   ".format(submission_count, error_count))
download(link_list)
