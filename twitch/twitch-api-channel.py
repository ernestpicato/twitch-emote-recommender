import datetime
from twitch import TwitchClient
import os
from EDA_Twitch_Data import ids
import json
import time
import numpy as np
import pandas as pd
import re

def datetime_handler(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()

client = TwitchClient(client_id = os.environ.get('CLIENT_ID'))

error = []

with open('twitch-info.json', 'w+') as f:
    for id in ids:
        try:
            channel = client.channels.get_by_id(id)
            data = json.dumps(channel, default=datetime_handler)
            f.write(data + "\n")
        except Exception, e:
            error.append((id, e))
            continue
        time.sleep(0.5)

# print error

# Copyright (c) [2017] [Tomaz Sifrer]
# https://github.com/tsifrer/python-twitch-client/blob/master/LICENSE
