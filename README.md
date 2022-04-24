# autopost
automatically post to reddit at a certain time

## prereqs
python3

## usage
`python autopost.py -s[--subreddit] <subreddit> -t[--title] <title> -p[--post] <post body> -x[--postTime] <time to post> -f[--flair] <flair> -l[--spoiler] <spoiler?> -v[--video] <video path> -g[--videogif] <gif-ify video?> -i[--image] <image path>`

```
ARGUMENTS:

   [REQUIRED] --subreddit : subreddit to post to
   [REQUIRED] --title : post title
   [REQUIRED]   one of the folowing
              --post : selftext post body
              --video : local video path to post
              --image : local image path to post
   [OPTIONAL] --postTime : local time to post (default 5:30am)
   [OPTIONAL] --flair : post flair - required sometimes by subreddit
   [OPTIONAL] --spoiler : provide if spoiler
   [OPTIONAL] --videogif : turn the video into a gif
```
example: `python autopost.py -s omnitest -t test -p post -l -x 03:40`
