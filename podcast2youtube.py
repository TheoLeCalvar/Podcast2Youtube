#!/bin/env python3

import os.path
import json
import feedparser
import shutil
import tempfile
import urllib.request
import subprocess
import youtube as yt

import argparse
from oauth2client import tools
from time import mktime

def download_file(url):
    with urllib.request.urlopen(url) as response:
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            shutil.copyfileobj(response, tmp_file)
            return tmp_file.name

def convert_to_video(path_audio, args):
    out_path=None
    with tempfile.NamedTemporaryFile(dir='/tmp', delete=True) as tmp_file:
        out_path= "%s.%s" % (tmp_file.name, args.extension)

    args=[
        args.ffmpeg,
        '-v', 'quiet',
        '-i', path_audio,
        '-f', 'image2',
        '-loop', '1',
        '-i', args.image,
        '-s', args.dimensions,
        '-c:v', 'libx264',
        '-crf', '18',
        '-tune', 'stillimage',
        '-preset', 'medium',
        '-shortest',
        out_path
    ]
    subprocess.run(args, check=True, stdout=subprocess.DEVNULL)
    return out_path

def upload_to_youtube(path_video, args):
    youtube=yt.get_authenticated_service(args)
    args.file=path_video

    video_id = yt.initialize_upload(youtube, args)
    if not args.playlist is None:
        yt.playlist_items_insert(youtube, {
                'snippet.playlistId': args.playlist,
                'snippet.resourceId.kind': 'youtube#video',
                'snippet.resourceId.videoId': video_id
            },
            part='snippet',
            onBehalfOfContentOwner='')


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(add_help=True,parents=[tools.argparser])

    argparser.add_argument("--url", required=True, help="Rss feed url")
    argparser.add_argument("--image", default='logo.png', help="Path to the background image")
    argparser.add_argument("--playlist", default=None, help='Playlist id')
    argparser.add_argument("--category", default="22")
    argparser.add_argument("--privacy", dest='privacyStatus', default='private', choices=['public', 'private', 'unlisted'])
    argparser.add_argument("--ffmpeg", default="ffmpeg")
    argparser.add_argument("--extension", default="mp4")
    argparser.add_argument("--dimensions", default="720x480")
    argparser.add_argument("--dbpath", default="latest.json")
    argparser.add_argument("--credentials", default="credentials.json")

    latest_post = 0

    args = argparser.parse_args()

    if os.path.isfile(args.dbpath):
        with open(args.dbpath, 'r') as f:
            latest_post = int(json.load(f)[0])
    
    new_latest=latest_post
    
    feed = feedparser.parse(args.url)

    for post in sorted(feed.entries, key=lambda p: mktime(p.published_parsed)):
        post_time = mktime(post.published_parsed)
        audio_path = None
        video_path = None

        if (post_time < latest_post):
            continue # ignore post issued before latest_post

        print("Processing %s" % (post.title))
        args.title = post.title
        args.description = post.summary
        args.keywords = ','.join([t.term for t in post.tags])


        for l in post.links:
            if (l.type == 'audio/mpeg'):
                audio_path = download_file(l.href)
                break

        print("Converting podcast to video")
        video_path = convert_to_video(audio_path, args)
        print("Uploading to youtube")
        upload_to_youtube(video_path, args)

        new_latest = max(new_latest, post_time)


    with open(args.dbpath, 'w') as f:
        json.dump([int(new_latest)],f)
