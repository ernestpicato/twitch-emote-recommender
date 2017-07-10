import datetime
from twitch import TwitchClient
import os
from EDA_Twitch_Data import ids
import json
import time
import numpy as np
import pandas as pd
import re
from chatreplay import chatreplay

def datetime_handler(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()

client = TwitchClient(client_id = os.environ.get('CLIENT_ID'))

test = [63577725]

error = []

with open('video-info.json', 'w+') as f:
    for id in test:
        try:
            video = client.channels.get_videos(id)
            for v in video:
                data = json.dumps(v, default=datetime_handler)
                f.write(data + "\n")
        except Exception, e:
            error.append((id, e))
            continue
        time.sleep(0.5)

# print error

video_data = pd.read_json('video-info.json', lines=True)

videos = []
for i in xrange(len(video_data)):
    videos.append(video_data['id'][i].encode('utf-8'))

chatreplay(videos)

chat = pd.read_table('videos/v60428514.txt', delimiter='\t', header=None, names=('datetime', 'viewer', 'text'), infer_datetime_format=True)
print chat

# Copyright (c) [2017] [Tomaz Sifrer]
# https://github.com/tsifrer/python-twitch-client/blob/master/LICENSE
