# Podcast2Youtube

A simple POC that downloads audio files from a RSS feed and uploads them on Youtube.

## Installation

This python script requires three python libraries `feedparser`, `google-api-python-client`, and `google-auth-oauthlib`.
You can install then with `pip install -r requirements.txt`.
It also need `ffmepg` to create the video.

## Configuration

First you need to obtain your credentials to use Google API.
Go [here](https://developers.google.com/youtube/registering_an_application) and follow the instructions.
Then complete `client_secrets.json` with your `client_id` and `client_secret`.


## Usage

```
usage: podcast2youtube.py [-h] [--auth_host_name AUTH_HOST_NAME]
                   [--noauth_local_webserver]
                   [--auth_host_port [AUTH_HOST_PORT [AUTH_HOST_PORT ...]]]
                   [--logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}] --url
                   URL [--image IMAGE] [--playlist PLAYLIST]
                   [--category CATEGORY] [--privacy {public,private,unlisted}]
                   [--ffmpeg FFMPEG] [--extension EXTENSION]
                   [--dimensions DIMENSIONS] [--dbpath DBPATH]
                   [--credentials CREDENTIALS]

optional arguments:
  -h, --help            show this help message and exit
  --auth_host_name AUTH_HOST_NAME
                        Hostname when running a local web server.
  --noauth_local_webserver
                        Do not run a local web server.
  --auth_host_port [AUTH_HOST_PORT [AUTH_HOST_PORT ...]]
                        Port web server should listen on.
  --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        Set the logging level of detail.
  --url URL             Rss feed url
  --image IMAGE         Path to the background image
  --playlist PLAYLIST   Playlist id
  --category CATEGORY
  --privacy {public,private,unlisted}
  --ffmpeg FFMPEG
  --extension EXTENSION
  --dimensions DIMENSIONS
  --dbpath DBPATH
  --credentials CREDENTIALS
```

The `url` argument is the only required parameter, it is the url of the RSS feed to parse.
When launched, the script search for new items on the RSS feed.
If new elements are found, it downloads the first audio file it finds, converts it to a video and uploads it to Youtube.
The timestamp of the newest item parsed is stored in a file to prevent reuploading already existing files.

This script should be used with cron like `0 * * * * <path>/podcast2youtube.py --url <url>  >/dev/null 2>&1` 
