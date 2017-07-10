import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
from custom_structures import sub_points
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
