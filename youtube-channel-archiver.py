#!/usr/bin/env python3

import requests
import os
import json
import time
from dotenv import load_dotenv
import yt_dlp

load_dotenv()
API_KEY = os.getenv('API_KEY')  # replace API_KEY with your own YouTube API key credentials
CHECK_INTERVAL = 3600  # check for new videos every 1 hour
OUTPUT_DIR = "/mnt/hdd/archive"
VIDEO_FORMAT = "bestvideo[ext=mp4]+bestaudio[ext=m4a]"


if API_KEY is None:
    print("Change the API_KEY variable in .env file with your own\nExample: API_KEY=\"AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\"")
    quit()

# read the list of channel IDs from a file
with open("channel_list.txt") as f:
    channel_ids = [line.strip() for line in f.readlines() if not line.startswith('#') and line.strip()]

# initialize a dictionary to store the last video ID for each channel
last_video_ids = {channel_id: "" for channel_id in channel_ids}

try:
    while True:
        for channel_id in channel_ids:
            try:
                # construct the API endpoint URL
                url = f"https://www.googleapis.com/youtube/v3/search?key={API_KEY}&channelId={channel_id}&part=snippet,id&order=date&maxResults=1&type=video,playlist"

                # make the API request
                response = requests.get(url)
                data = json.loads(response.text)

                # print out the data variable for debugging purposes
                print(json.dumps(data, indent=4))

                if "items" not in data:
                    print("Error in API response:", data)
                    continue

                # get the channel name after get the video ID or playlist ID of the most recent content
                channel_name = data["items"][0]["snippet"]["channelTitle"]
                if "videoId" in data["items"][0]["id"]:
                    content_id = data["items"][0]["id"]["videoId"]
                    content_type = "video"
                elif "playlistId" in data["items"][0]["id"]:
                    content_id = data["items"][0]["id"]["playlistId"]
                    content_type = "playlist"
                else:
                    print(f"No video or playlist found for channel {channel_name}")
                    continue

                # Check if the channel directory exists in the output directory
                channel_dir = os.path.join(OUTPUT_DIR, channel_name)

                # Set yt-dlp options
                ydl_opts = {
                    'format': VIDEO_FORMAT,
                    'outtmpl': os.path.join(channel_dir, f'%(title)s.%(id)s.%(ext)s'),
                    'quiet': False
                }
                root_channel_dir = channel_dir
                ydl_opts_playlist = {
                    'format': VIDEO_FORMAT,
                    'outtmpl': os.path.join(root_channel_dir, f'%(playlist_title)s/%(title)s.%(id)s.%(ext)s'),
                    'quiet': False
                }
                ydl = yt_dlp.YoutubeDL(ydl_opts)
                ydlp = yt_dlp.YoutubeDL(ydl_opts_playlist)

                if not os.path.exists(channel_dir):
                    while True:
                        a = input("New Channel detected would you like to download all videos? [Y/n]")
                        if a == "y" or a == "" or a == "Y":
                            print("Downloading all videos")

                            ydl.download([f"https://www.youtube.com/channel/{channel_id}/videos"])

                        elif a == "n" or a == "N":
                            break
                        else:
                            print("Enter either y or n")

                    while True:
                        a = input("Would you like to download all playlist created by the channel? [Y/n]")
                        if a == "y" or a == "" or a == "Y":
                            print("Downloading all playlists")

                            ydlp.download([f"https://www.youtube.com/channel/{channel_id}/playlists"])

                        elif a == "n" or a == "N":
                            break
                        else:
                            print("Enter either y or n")

                # check if the video ID has changed
                if content_id != last_video_ids[channel_id]:
                    print(f"New video detected on channel {channel_name}!")

                    # download the video using yt-dlp
                    ydl.download([f'https://www.youtube.com/watch?v={content_id}'])

                    last_video_ids[channel_id] = content_id
                else:
                    print("No new videos sleeping for 1 hour")

            except Exception as e:
                print(f"Error occurred for channel {channel_name}: {e}")

        time.sleep(CHECK_INTERVAL)

except KeyboardInterrupt:
    print("\nQuitting the program gracefully.")
