# Twitch Emote Recommender

This project was developed as a capstone project for the Galvanize Data Science Immersive program. Try out the application [here](http://twitch-emote-recommender-pro.herokuapp.com/).

### Fundamentals of Twitch.tv:

Twitch.tv is the world's leading social video platform and community for gamers. The two main activities for viewers include watching the broadcaster as well as interacting with the community through chat. This project focused on the latter.

Becoming a Twitch.tv broadcaster is as simple as setting up an account. After maintaining a certain viewership level, broadcasters can apply for partnership that allows their channel's followers to support the channel by subscribing. Subscriptions come in 3 tiers ($4.99, $9.99, and $24.99), with the most tangible incentive for the viewer coming in the form of emotes. Of the 2+ million active broadcasters, 17000+ are partners.  

### Business Opportunity/Project Motivation:

So, why should viewers and followers subscribe to a channel? Well, emojis, emoticons, emotes, whatever you want to call them, can convey emotion or whole sentences in just a single image. This is very powerful for Twitch.tv chat because it can move very quickly at times, and emotes help in facilitating communication. Conveniently enough, subscribing monthly to a channel gives you access to exclusive and unique emotes that can be used throughout Twitch.tv.

In contrast to Twitch.tv's current discovery directory that recommends channels based on a viewer's history, the Twitch Emote Recommender serves as a serendipitous recommender that works on the assumption that the viewer may want to be surprised by the unexpected. Based solely on a channel's set of emotes, channels are recommended depending on their similarity to another channel's emotes.

### Data Collection and Cleaning:

13777 partner channel ids were collected from the twitchemotes.com API. Using these ids, requests were made to the Twitch.tv API to get additional information like channel age and number of followers. Channels that had changed urls, had their emotes removed, or violated Terms of Service (TOS) were removed, with 13526 channels retained (98.2%). The distribution of emotes per channel is right skewed:

<p align="center">
<img src="https://github.com/ernestpicato/twitch-emote-recommender/blob/master/twitch/emotes/num_emotes.png" width="400" height="300">
</p>

<p align="center">
<img src="https://github.com/ernestpicato/twitch-emote-recommender/blob/master/twitch/emotes/num_emotes_extended.png" width="400" height="300">
</p>

### Data Modeling, Validation, and Presentation (App):

Twitch.tv partner channel recommender based on emotes.

### Future Work:

Twitch.tv partner channel recommender based on emotes.
