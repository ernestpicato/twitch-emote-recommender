# Twitch Emote Recommender

This project was developed as a capstone project for the Galvanize Data Science Immersive program. Try out the application [here](http://twitch-emote-recommender-pro.herokuapp.com/).

### Fundamentals of Twitch.tv:

Twitch.tv is the world's leading social video platform and community for gamers. The two main activities for viewers include watching the broadcaster as well as interacting with the community through chat. This project focused on the latter.

Becoming a Twitch.tv broadcaster is as simple as setting up an account. After maintaining a certain viewership level, broadcasters can apply for partnership that allows their channel's followers to support the channel by subscribing. Subscriptions come in 3 tiers ($4.99, $9.99, and $24.99), with the most tangible incentive for the viewer coming in the form of emotes. Of the 2+ million active broadcasters, 17000+ are partners.  

### Business Opportunity/Project Motivation:

So, why should viewers and followers subscribe to a channel? Well, emojis, emoticons, or emotes can convey emotion or whole sentences in just a single image. This is very powerful for Twitch.tv chat because it can move very quickly at times, and emotes help in facilitating communication. Conveniently enough, subscribing monthly to a channel gives you access to exclusive and unique emotes that can be used throughout Twitch.tv.

In contrast to Twitch.tv's current discovery directory that recommends channels based on a viewer's history, the Twitch Emote Recommender serves as a serendipitous recommender that works on the assumption that the viewer may want to be surprised by the unexpected. Based solely on a channel's set of emotes, channels are recommended depending on their similarity to another channel's emotes.

### Data Collection and Cleaning:

13777 partner channel ids were collected from the twitchemotes.com API. Using these ids, requests were made to the Twitch.tv API to get additional information like channel age and number of followers. Channels that had changed urls, had their emotes removed, or violated Terms of Service (TOS) were removed, with 13526 (98.2%) channels retained. The distribution of emotes per channel is right skewed:

<p align="center">
<img src="https://github.com/ernestpicato/twitch-emote-recommender/blob/master/twitch/emotes/num_emotes.png" width="400" height="300">
</p>

The emotes for each channel were then parsed to extract the main context of each emote. For example, lirikSALT, lirikLEWD, and lirikBLIND were parsed into salt, lewd, and blind. For 282 (2.1%) channels, the prefixes were manually parsed. The most common emotes were rage, love, and hype:  

<p align="center">
<img src="https://github.com/ernestpicato/twitch-emote-recommender/blob/master/twitch/emotes/emotes_extended.png" width="400" height="300">
</p>

### Data Modeling, Validation, and Presentation (App):

The first model was built by transforming the emotes into tf-idf vectors and using cosine to measure similarity. A second model was built using Latent Dirichlet Allocation (LDA) to find groups of related emotes and using Euclidean distance to measure similarity. For the sake of project completion, only the first model was implemented for validation.

So, how are the recommendations validated? Well, it goes back to the problem the recommender is attempting to solve. In order to measure how serendipitous a recommendation is for a viewer, the best way to validate is to ask the users themselves what they think. To act as an interface for this interaction, a Flask web-app was deployed to Heroku that referenced PostgreSQL databases. The validation pipeline for each channel's top 10 recommended channels was also created in the form of an A/B test where follower/subscriber flow could be measured with and without the recommender.  

### Future Work:

In the future, getting responses from viewers regarding the recommendations would be paramount. Additionally, if the recommender proves to be beneficial, the second model can be implemented to see how the recommendations shift. An issue with just working with the emote names themselves is that some broadcasters default to naming their emotes with 1, 2, 3 or A, B, C. It is really like how in programming variable names should be simple yet descriptive. This is where the model could incorporate the images themselves since the context of the image is likely needed to decipher what the broadcaster is trying to express. Likewise, a different angle on the project could develop in the sense that instead of recommending channels based on emotes, emotes can be recommended to broadcasters.  
