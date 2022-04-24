# autopost
automatically post to reddit at a certain time

## prereqs
python3

## usage
`python autopost.py -s[--subreddit] <subreddit> -t[--title] <title> -p[--post] <post body> -x[--postTime] <time to post> -f[--flair] <flair> -l[--spoiler] <spoiler?> -v[--video] <video path> -g[--videogif] <gif-ify video?> -i[--image] <image path>`

```
ARGUMENTS:

   [REQUIRED] --subreddit : subreddit to post to
   [REQUIRED] --title     : post title
   [REQUIRED]   one of the folowing
              --post      : selftext post body
              --video     : local video path to post
              --image     : local image path to post
   [OPTIONAL] --postTime  : local time to post (default 5:30am)
   [OPTIONAL] --flair     : post flair - required sometimes by subreddit
   [OPTIONAL] --spoiler   : provide if spoiler
   [OPTIONAL] --videogif  : turn the video into a gif
```
example: `python autopost.py -s eldenring -t "Godskin Duo takes 16954 damage in one hit and dies instantly" -v "godskin insta.mp4" -g -l -f Spoilers`

![image](https://user-images.githubusercontent.com/4252190/164974868-3811e873-11d0-4209-a835-053fa574d3bd.png)
