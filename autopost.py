import praw
import time
import sys
import getopt
import pyfiglet
  
def usage(throw=True):
    print("Usage: python autopost.py -s[--subreddit] <subreddit> -t[--title] <title> -p[--post] <post body> -x[--postTime] <time to post> -f[--flair] <flair> -l[--spoiler] <spoiler?> -v[--video] <video path> -g[--videogif] <gif-ify video?> -i[--image] <image path>")
    if throw:
        raise

title = ''
body = ''
post_time = '05:30'
subname = ''
flair = ''
spoiler = False
gif = False
video = ''
image = ''

try:
    opts, args = getopt.getopt(sys.argv[1:], 's:t:p:x:f:l:v:g:i:h', ['subreddit=', 'title=', 'post=', 'postTime=', 'flair=', 'spoiler=', 'video=', 'videogif=', 'image=', 'help'])
except getopt.GetoptError:
    usage()

for opt, arg in opts:
    if opt in ('-h', '--help'):
        usage(False)
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
    elif opt in ('-l', '--spoiler'):
        spoiler = bool(arg)
    elif opt in ('-v', '--video'):
        video = arg
    elif opt in ('-g', '--videogif'):
        gif = bool(arg)
    elif opt in ('-i', '--image'):
        image = arg
    else:
        usage()

if len([x for x in [body, image, video] if x != '']) > 1:
    print('Must only provide one of -p, -v, or -i')
    sys.exit(2)

post_type = ''
if body != '':
    post_type = 'text'
elif video != '':
    post_type = 'video'
else:
    post_type = 'image'

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

now = time.localtime()
current_time = time.strftime("%H:%M", now)

print(pyfiglet.figlet_format("AUTOPOST", font = "slant"))
print('local time: ' + current_time)
print('Getting info for sub...')

if sub is None or sub.display_name == '':
    print("subreddit " + subname + " not found.")
    sys.exit(2)

if sub.post_requirements()['is_flair_required'] and flair == '':
    print('flair required for this subreddit.')
    sys.exit(2)

print('subreddit: ' + sub.display_name)
print('sub description sample: ' + sub.description.split("\n")[0])

posted = False
while not posted:
    if current_time == post_time:
        match post_type:
            case 'text':
                if flair == '':
                    sub.submit(title, selftext=body, spoiler=spoiler)
                else:
                    choices = list(sub.flair.link_templates.user_selectable())
                    template_id = next(x for x in choices if x["flair_text"] == flair)["flair_template_id"]
                    sub.submit(title, selftext=body, flair_id=template_id, spoiler=spoiler)
            case 'video':
                if flair == '':
                    sub.submit_video(title, video_path=video, videogif=gif, spoiler=spoiler)
                else:
                    choices = list(sub.flair.link_templates.user_selectable())
                    template_id = next(x for x in choices if x["flair_text"] == flair)["flair_template_id"]
                    sub.submit_video(title, video_path=video, videogif=gif, flair_id=template_id, spoiler=spoiler)
            case 'image':
                if flair == '':
                    sub.submit_image(title, image_path=image, spoiler=spoiler)
                else:
                    choices = list(sub.flair.link_templates.user_selectable())
                    template_id = next(x for x in choices if x["flair_text"] == flair)["flair_template_id"]
                    sub.submit_image(title, image_path=image, flair_id=template_id, spoiler=spoiler)
        posted = True
        print('Posted!')
    else:
        print('Not yet ' + post_time + '. Waiting another 60 seconds...')
        time.sleep(60)