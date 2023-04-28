#!/bin/sh
[ -z "$2" ] && printf "Usage: $0 <handle without the @> <YOUTUBE_API_KEY>\n" && exit

curl -XGET "https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=25&q=%40'$1'&type=channel&key="$2|jq|grep channelId*
