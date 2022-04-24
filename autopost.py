import praw
import time
import sys
import getopt

def usage():
    print("Usage: python autopost.py -s[--subreddit] <subreddit> -t[--title] <title> -p[--post] <post body> -x[--postTime] <time to post>")

title = ''
body = ''
post_time = '5:30'
subname = ''

try:
    opts, args = getopt.getopt(sys.argv[1:], 's:t:p:x:h', ['subreddit=', 'title=', 'post=', 'postTime=', 'help'])
except getopt.GetoptError:
    usage()
    sys.exit(2)

for opt, arg in opts:
    if opt in ('-h', '--help'):
        usage()
        sys.exit(2)
    elif opt in ('-t', '--title'):
        title = arg
    elif opt in ('-p', '--post'):
        body = arg
    elif opt in ('-x', '--postTime'):
        post_time = arg
    elif opt in ('-s', '--subreddit'):
        subname = arg
    else:
        usage()
        sys.exit(2)

if title == '' or body == '' or subname == '':
    print('Subreddit, title and body required.')
    usage()
    sys.exit(2)

f = open('./creds.txt')

# format is <user>,<pwd>,<id>,<secret>,<user_agent> 
creds = f.read().split(",")
if len(creds) < 5:
    print("Missing credential file 'creds.txt'")
    sys.exit(2)

reddit = praw.Reddit(
    client_id=creds[2],
    client_secret=creds[3],
    user_agent=creds[4],
    username=creds[0], 
    password=creds[1]
)

sub = reddit.subreddit(subname)
posted = False

print('Getting info for sub ' + subname + '...')
if sub is None or sub.display_name == '':
    print("subreddit " + subname + " not found.")
    sys.exit(2)

print('subreddit: ' + sub.display_name)
print('description: ' + sub.description.split("\n")[0])


while not posted:
    now = time.localtime()
    current_time = time.strftime("%H:%M", now)
    
    if current_time is post_time:
        sub.submit(title, body)
        posted = True
        print('Posted!')
    else:
        print('Not yet ' + post_time + '. Waiting another 60 seconds...')
        time.sleep(60)