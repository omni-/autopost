import praw
import time
import sys
import getopt

def usage():
    print("Usage: python autopost.py -s[--subreddit] <subreddit> -t[--title] <title> -p[--post] <post body> -x[--postTime] <time to post> -f[--flair] <flair> -i[--spoiler] <is spoiler?>")
    raise

title = ''
body = ''
post_time = '05:30'
subname = ''
flair = ''
spoiler = False

try:
    opts, args = getopt.getopt(sys.argv[1:], 'f:i:s:t:p:x:h', ['subreddit=', 'title=', 'post=', 'postTime=', 'help'])
except getopt.GetoptError:
    usage()

for opt, arg in opts:
    if opt in ('-h', '--help'):
        usage()
    elif opt in ('-t', '--title'):
        title = arg
    elif opt in ('-p', '--post'):
        body = arg
    elif opt in ('-x', '--postTime'):
        post_time = arg
    elif opt in ('-s', '--subreddit'):
        subname = arg
    elif opt in ('-f', '--flair'):
        flair = arg
    elif opt in ('-i', '--spoiler'):
        spoiler = bool(arg)
    else:
        usage()

if title == '' or body == '' or subname == '':
    print('Subreddit, title and body required.')
    usage()

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
reddit.validate_on_submit = True
sub = reddit.subreddit(subname)
posted = False

print('Getting info for sub ' + subname + '...')
if sub is None or sub.display_name == '':
    print("subreddit " + subname + " not found.")
    sys.exit(2)

if sub.post_requirements()['is_flair_required'] and flair == '':
    print('flair required for this subreddit.')
    sys.exit(2)

print('subreddit: ' + sub.display_name)
print('first line of sub description: ' + sub.description.split("\n")[0])


while not posted:
    now = time.localtime()
    current_time = time.strftime("%H:%M", now)
    print('local time: ' + current_time)
    
    if current_time == post_time:
        if flair == '':
            sub.submit(title, selftext=body, spoiler=spoiler)
        else:
            choices = list(sub.flair.link_templates.user_selectable())
            template_id = next(x for x in choices if x["flair_text"] == flair)["flair_template_id"]
            sub.submit(title, selftext=body, flair_id=template_id, spoiler=spoiler)
        posted = True
        print('Posted!')
    else:
        print('Not yet ' + post_time + '. Waiting another 60 seconds...')
        time.sleep(60)