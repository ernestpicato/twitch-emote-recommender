import os
import urllib
import json

def emote_retrieval(channels):
    '''
    Input: LIST of Twitch.tv channel names
    Output: Directory of .png files

    Returns a directory of the subscriber emotes for the specified channels
    '''
    # Check to see if there is an emotes directory in the current directory,
    # and creates one if it does not exist
    if not os.path.exists('./app/twitch-app/static/emotes'):
        os.makedirs('./app/twitch-app/static/emotes')
    print('Saving emotes to folder: ' + os.path.abspath('./app/twitch-app/static/emotes') + '...')
    print('Grabbing emote list...')

    # Get all the Twitch emotes from the API
    response = urllib.urlopen('https://api.twitch.tv/kraken/chat/emoticons/')
    emotes = json.load(response)

    for channel in channels:

        # Get a list of the subscriber emotes for a channel; custom API courtesy of
        # Alex Thomassen: https://blog.decicus.com/custom-apis/
        channel = urllib.urlopen('https://decapi.me/twitch/subscriber_emotes?channel=' + channel)

        for image in channel:
            emojis = image.split()

        # For each emote, access and retrieve the .png file and store it in the
        # emotes directory
        for i in xrange(len(emotes['emoticons'])):
            for emoji in emojis:
                try:
                    if emotes['emoticons'][i]['regex'] == emoji:
                        print 'Downloading: {}...'.format(emotes['emoticons'][i]['regex'])
                        urllib.urlretrieve(emotes['emoticons'][i]['images'][0]['url'], './app/twitch-app/static/emotes/' + emotes['emoticons'][i]['regex'] + '.png')
                except Exception:
                    print 'Unable to retrieve {} due to formatting'.format(emotes['emoticons'][i]['regex'])
                    continue

    print('Done! Kappa')

if __name__ == '__main__':
    channels = ['thebuddha3', 'demarokkaantje', 'grendler', 'pipepunklive']
    emote_retrieval(channels)
