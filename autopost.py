import praw
import time
import sys
import getopt
import pyfiglet
import os
import platform
from termcolor import colored

if platform.system() == 'Windows':
    os.system('color')
  
def usage():
    print(colored("Usage: python autopost.py -s[--subreddit] <subreddit> -t[--title] <title> -p[--post] <post body> -x[--postTime] <time to post> -f[--flair] <flair> -l[--spoiler] <spoiler?> -v[--video] <video path> -g[--videogif] <gif-ify video?> -i[--image] <image path>", 'red'))

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
    opts, args = getopt.getopt(sys.argv[1:], 's:t:p:x:f:lv:gi:h', ['subreddit=', 'title=', 'post=', 'postTime=', 'flair=', 'spoiler', 'video=', 'videogif', 'image=', 'help'])
except getopt.GetoptError:
    print('Getopts error')
    usage()
    raise

for opt, arg in opts:
    if opt in ('-h', '--help'):
        usage()
        sys.exit(0)
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
        spoiler = True
    elif opt in ('-v', '--video'):
        video = arg
    elif opt in ('-g', '--videogif'):
        gif = True
    elif opt in ('-i', '--image'):
        image = arg
    else:
        usage()
        raise "Unrecognized option."

if len([x for x in [body, image, video] if x != '']) > 1:
    raise 'Must only provide one of -p, -v, or -i'

post_type = ''
if body != '':
    post_type = 'text'
elif video != '':
    post_type = 'video'
else:
    post_type = 'image'

if title == '' or subname == '':
    usage()
    raise 'Subreddit and title required'

f = open('./creds.txt')

# format is <user>,<pwd>,<id>,<secret>,<user_agent> 
creds = f.read().split(",")
if len(creds) < 5:
    raise "Missing credential file 'creds.txt'"

reddit = praw.Reddit(
    client_id=creds[2],
    client_secret=creds[3],
    user_agent=creds[4],
    username=creds[0], 
    password=creds[1]
)
reddit.validate_on_submit = True
sub = reddit.subreddit(subname)

clear = lambda: os.system('cls' if platform.system() == 'Windows' else 'clear')
clear()

print(colored(pyfiglet.figlet_format("AUTOPOST", font = "slant"), 'blue'))

print('|', colored('getting info for sub...', 'green'))

if sub is None or sub.display_name == '':
    raise ("subreddit " + subname + " not found.")

if sub.post_requirements()['is_flair_required'] and flair == '':
    raise 'flair required for this subreddit.'

now = time.localtime()
current_time = time.strftime("%H:%M", now)

print('| + ', colored('subreddit: ', 'yellow') + colored(sub.display_name, 'cyan'))
print('| + ', colored('description: ', 'yellow') + colored(sub.description.split("\n")[0], 'cyan'))
print()
print('|', colored('getting post info...', 'green'))
print('| + ', colored('local time: ', 'yellow') + colored(current_time, 'cyan'))
print('| + ', colored('post title: ', 'yellow') + colored(title, 'cyan'))
print('| + ', colored('post type: ', 'yellow') + colored(post_type, 'cyan'))
print('| + ', colored('image path: ', 'yellow') + colored(image, 'cyan'))
print('| + ', colored('video path: ', 'yellow') + colored(video, 'cyan'))
print('| + ', colored('flair: ', 'yellow') + colored(flair, 'cyan'))
print('| + ', colored('videogif: ', 'yellow') + colored(gif, 'cyan'))
print()
print('| ============================================================== |')

posted = False
while not posted:
    now = time.localtime()
    current_time = time.strftime("%H:%M", now)
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
        print(colored('>>> Posted! <<<', 'green'))
    else:
        print('|', colored('not yet', 'yellow'), colored(post_time, 'cyan'), colored('(currently', 'yellow'), colored(current_time, 'cyan') + colored('). Waiting another 60 seconds...', 'yellow'), '|')
        time.sleep(60)