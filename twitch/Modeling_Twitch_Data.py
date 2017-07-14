import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict
import matplotlib.pyplot as plt
from custom_structures import sub_points
import urllib
import json
from gensim import corpora, models
import gensim

# Create a dataframe from the pre-processed combination of twitchemotes.com
# and Twitch.tv APIs
df = pd.read_json('twitch-data.json')

# Reset index necessary after converting a dataframe to a .json file and then to
# dataframe again
df.reset_index(drop=True, inplace=True)

# List of lists of all the emotes for each channel
channel_emotes = []
for i in xrange(len(df)):
    channel_emotes.append(df.iloc[i]['emotes_parsed'])

# tf-idf and cosine similarity for the emotes (NEED TO SPLIT INTO TRAIN, VALIDATION, TEST SETS)
v = TfidfVectorizer(tokenizer=lambda i:i, lowercase=False)
x = v.fit_transform(channel_emotes)
similarities = cosine_similarity(x)

# Getting the 10 most similar channels for each channel (includes the specified channel)
most_sim = {}
for i in xrange(len(similarities)):
    for row in similarities[i:i+1]:
        most = row.argsort()[-10:]
        most_sim[i] = most

df['recommendations'] = df.index.to_series().map(most_sim)

# Getting the indices for the 10 most similar channels for each channel (includes the specified channel)
index_channel = {}
for i in xrange(len(df)):
    index_channel[i] = df['name'].iloc[i].encode('utf-8')

# Getting the channel names for the 10 most similar channels for each channel (includes the specified channel)
recommendations = defaultdict(list)
for i in xrange(len(df)):
    for value in df['recommendations'].iloc[i]:
        recommendations[i].append(df['name'].iloc[value].encode('utf-8'))

df['recommended_channel_names'] = df.index.to_series().map(recommendations)

# Preparing the dataframe for conversion to a .csv file (to be made into a table in sqlite3 database)
df_reduced = df.drop(['display_name', 'emotes', 'emotes_parsed', 'prefix', 'broadcaster_language', 'language', 'description', 'followers', 'views', 'mature', 'game', 'status', 'created_at', 'updated_at'], axis=1)

# PUtting recommendations into their own columns
df_reduced[['rec1','rec2','rec3','rec4', 'rec5','rec6', 'rec7','rec8', 'rec9','rec10']] = pd.DataFrame([x for x in df_reduced['recommended_channel_names']])

df_reduced = df_reduced.drop(['recommendations', 'recommended_channel_names'], axis=1)

app_csv = df_reduced.to_csv('twitch.csv', index=False)

-------------------------------------------------

# Getting emote urls
response = urllib.open('https://api.twitch.tv/kraken/chat/emoticons')
emotes = json.load(response)

img_urls = pd.DataFrame.from_dict(emotes['emoticons'])

urls = {}
for i in xrange(len(img_urls)):
    urls[img_urls.iloc[i]['regex']] = img_urls.iloc[i]['images'][0]['url']

# Putting all the emotes into a list
imgs = []
for i in xrange(len(df)):
    for j in xrange(len(df['emotes'].iloc[i])):
        imgs.append((df['name'].iloc[i], df['emotes'].iloc[i][j]))

channel = []
img = []
for value in imgs:
    ch, em = value
    channel.append(ch)
    img.append(em)

# Getting dataframe of channels with their corresponding emotes and urls
df_url_p1 = pd.DataFrame({'channel':channel})
df_url_p2 = pd.DataFrame({'emote':img})
df_url = pd.concat([df_url_p1, df_url_p2], axis=1)
df_url['url'] = df_url['emote'].map(urls)

# 2235 emotes are obsolete (used deprecated version of twitchemotes.com API)
df_url.dropna(inplace=True)
# 102735 of 104970 emotes retained
df_url.reset_index(drop=True, inplace=True)

# Getting the total count for each emote across all channels
emojis = {}
for i in xrange(len(df)):
    emotes = df['emotes_parsed'].iloc[i]
    for emote in emotes:
        emojis[emote] = emojis.get(emote, 0) + 1

# Getting the words that have a count greater than the specified value and visualizing them
words = {}
for key, value in emojis.iteritems():
    if value > 650:
        words[key] = value

plt.bar(range(len(words)), words.values(), align='center')
plt.xticks(range(len(words)), words.keys())
plt.show()

# Getting the number of emotes for each channel
num_emotes = {}
for i in xrange(len(df)):
    num_emotes[df['name'].iloc[i].encode('utf-8')] = len(df['emotes'].iloc[i])

df['num_emotes'] = df['name'].map(num_emotes)

# Based on the number of emotes for each channel, specify the range of subscription
# points that channel can have
df['sub_points'] = df['num_emotes']
df['sub_points'] = df['sub_points'].replace(sub_points)

# List of lists of all the emotes for each channel (encoded)
texts = []
for i in xrange(len(df)):
    channel = []
    for j in xrange(len(df['emotes_parsed'].iloc[i])):
        channel.append(df['emotes_parsed'].iloc[i][j].encode('utf-8'))
    texts.append(channel)

# LDA for the emotes
dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=100, id2word=dictionary, passes=20)
print(ldamodel.print_topics(num_topics=100, num_words=4))
