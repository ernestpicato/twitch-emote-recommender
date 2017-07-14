import numpy as np
import pandas as pd
import re
from collections import defaultdict
from custom_structures import suspended_accounts, wrong_dict

# Create a dataframe from the twitchemotes.com API (cached data from version 2 on
# 06/28/2017; version 2 only returns static content, and was deprecated as of 07/07/2017)
# If time permits, update content with version 3 (emotes more up to date)
# 13777 Twitch.tv partners (start)
df = pd.read_json('twitch-emote-api-cached-data.json')

# df.columns: channels, meta, template, unknown_emotes; only channels column is relevant
df_channels = df['channels']

# First two channels were Twitch-Curse Integration and Twitch Turbo and Prime
# 13775 Twitch.tv partners remaining
df_ch_without_twitch = df_channels.iloc[2:]

# 5 channels had no values
# 13770 Twitch.tv partners remaining
df_ch_without_twitch_nan = df_ch_without_twitch.dropna()

# From the subscriber emote cached data, get the channel ids
ids = []
for i in xrange(len(df_ch_without_twitch_nan)):
    ids.append(df_ch_without_twitch_nan[i]['channel_id'])

# Export ids to twitch-api-channel.py; calls to Twitch.tv API for channel information)
# 49 channels had 422 error client (channel suspended for violation(s))
# 13721 Twitch.tv partners remaining
indices_to_drop = []
for i in xrange(len(df_ch_without_twitch_nan)):
    for account in suspended_accounts:
        if df_ch_without_twitch_nan.iloc[i]['channel_id'] == account:
            indices_to_drop.append(i)

df_clean = df_ch_without_twitch_nan.drop(df_ch_without_twitch_nan.index[indices_to_drop])
df_clean = pd.DataFrame({'name1':df_clean.index, 'information':df_clean.values})

# Create a dataframe from the Twitch.tv API
api_data = pd.read_json('twitch-info.json', lines=True)

# Combine the two dataframes and drop any broadcasters that were not partners
# (affiliates; are small channels offered 1 emote and other perks to grow channel, 10)
# or had changed urls (had emotes, but removed nonetheless, 175)
# 13536 Twitch.tv partners remaining
df_both = pd.concat([df_clean, api_data], axis=1)
df_both = df_both[df_both['partner'] == True]
df_both = df_both.drop(['name1', 'broadcaster_type', 'partner', 'logo', 'profile_banner', 'profile_banner_background_color', 'video_banner'], axis=1)

# Get the emotes for each channel
channel_emotes = {}
for i in xrange(len(df_both)):
    emojis = []
    for j in xrange(len(df_both['information'].iloc[i]['emotes'])):
        emoji = df_both['information'].iloc[i]['emotes'][j]['code'].encode('utf-8')
        emojis.append(emoji)
    channel_emotes[df_both['name'].iloc[i].encode('utf-8')] = emojis

df_both['emotes'] = df_both['name'].map(channel_emotes)

# Parse the emotes by splitting the first emote by capital letter and using the
# first item in split as word to split the rest of the emotes by
df_pre = df_both[['name', 'emotes']]

pre_emote = []
rmv_pre = defaultdict(list)
for term in df_pre['emotes']:
    w = re.sub( r"([A-Z])", r" \1", term[0]).split()[0]
    pre_emote.append(w)
    for word in term:
        rmv_pre[w].append(re.split(w, word)[-1].lower())

pre_emote = pd.Series(pre_emote)
df_pre['prefix'] = pre_emote.values
df_pre['emotes_clean'] = df_pre['prefix'].map(rmv_pre)

# If '' is in the dictionary values, flag that channel and evaluate afterwards
pre_wrong = {}
for key, value in rmv_pre.iteritems():
    if value[0] == '':
        pre_wrong[key] = 1
    else:
        pre_wrong[key] = 0

df_pre['prefix_wrong'] = df_pre['prefix'].map(pre_wrong)
df_pre.drop(['name', 'emotes'], axis=1, inplace=True)
df_extended = pd.concat([df_both, df_pre], axis=1)

# 282 channels manually adjusted (10 removed for incorrect emotes or emotes no
# longer available; 6 adjusted for the emote parsed incorrectly (prefix occurs
# more than once in an emote))
# 13526 Twitch.tv partners (end)
# See which prefixes were wrong, manually adjust the prefix
df_wrong = df_extended[df_extended['prefix_wrong'] == 1]
df_extended['prefix'] = df_extended['prefix'].replace(wrong_dict)

# Use new prefixes to adjust the emotes that were incorrectly parsed
df_extended_prefix = df_extended[['name', 'prefix', 'emotes']]
rmv_pre_extended = defaultdict(list)
for i in xrange(len(df_extended_prefix)):
    w = df_extended_prefix['prefix'].iloc[i]
    for term in df_extended_prefix['emotes'].iloc[i]:
        rmv_pre_extended[w].append(re.split(w, term)[-1].lower())

# Checking again to see if a channel has to be flagged
pre_wrong_extended = {}
for key, value in rmv_pre_extended.iteritems():
    if value[0] == '':
        pre_wrong_extended[key] = 1
    else:
        pre_wrong_extended[key] = 0

df_extended['emotes_clean_extended'] = df_extended['prefix'].map(rmv_pre_extended)
df_extended['prefix_wrong_extended'] = df_extended['prefix'].map(pre_wrong_extended)

# The 16 channels that need to be removed or manually adjusted again
df_wrong_extended = df_extended[df_extended['prefix_wrong_extended'] == 1]

# The 6 channels that had to be adjusted due to the prefix occurring more than once in an emote
df_extended['emotes_clean_extended'].loc[2066] = ['vamocnb', 'blumer']
df_extended['emotes_clean_extended'].loc[5183] = ['shill', 'hi', 'cheer', 'topdeck', 'fun', 'fail', 'rip', 'not', 'p', 'gold']
df_extended['emotes_clean_extended'].loc[6329] = ['biguin', 'uin', 'kk']
df_extended['emotes_clean_extended'].loc[8639] = ['ngoats', 'surprise', 'rekt', 'hey', 'rage', 'smirk', 'bert', 'goat', 'c', 'n', 'sorry', 'gasm', 'tissue', 'choke', 'cc', 'ccc', 'p', 'kill', 's', 'weeb', 'l', 'z']
df_extended['emotes_clean_extended'].loc[11482] = ['bars', 'littletimmy']
df_extended['emotes_clean_extended'].loc[13432] = ['lecagoule', 'teamgh']

# The 10 channels that had to be adjusted due to incorrect emotes or emotes no
# longer available
df_final = df_extended[(df_extended['display_name'] != 'BeyondTheSummit') \
                        & (df_extended['display_name'] != 'Fahr3nh3iT_') \
                        & (df_extended['display_name'] != 'GangstaZomber') \
                        & (df_extended['display_name'] != 'HiRezTV') \
                        & (df_extended['display_name'] != 'idrajit') \
                        & (df_extended['display_name'] != 'IPLAYWINNER') \
                        & (df_extended['display_name'] != 'JuAnGoTeM') \
                        & (df_extended['display_name'] != 'Ozrak') \
                        & (df_extended['display_name'] != 'ThePremierLeague') \
                        & (df_extended['display_name'] != 'Victorious Gaming')]

# Cleaning up the dataframe and then saving it to a .json file
df_final = df_final.drop(['information', 'emotes_clean', 'prefix_wrong', 'prefix_wrong_extended'], axis=1)
df_final = df_final.rename(columns = {'emotes_clean_extended': 'emotes_parsed'})
df_final.reset_index(drop=True, inplace=True)
df_final.to_json('twitch-data.json')

# For use with version 3 of twitchemotes.com API
# import urllib
#
# response = urllib.urlopen('https://twitchemotes.com/api_cache/v3/subscriber.json')
#
# twitchemotes = pd.read_json(response)
# twitchemotes = twitchemotes.T
# partners = twitchemotes[twitchemotes['broadcaster_type']=='partner']
