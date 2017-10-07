'''
This bot is titled as EVE the event bot. This bot uses Facebook's GraphAPI to extract data from Facebook Pages. The user inputs his choice and the output of the category of 
events is given respectively. GraphAPI runs dynamically and the events are stored in a database file which is in the same repository of the bot. The database is prepopulated
with events which are held on a regular basis and this helps the developers to maintain stringent quality control. The database also includes some of the most happening events.
'''


# imports all the necessary files to run the bot
import urllib
import time, sys
import telepot, facebook, requests
from telepot.loop import MessageLoop
from events_database import database
from telepot import DelegatorBot
from telepot.delegate import pave_event_space, per_chat_id, create_open
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton


# Token file is prepopulated and is included in the repository. This token file can be replaced with a custom key. 
with open('TOKEN.txt', 'r') as token_file:
    TOKEN = token_file.read()

#A user access token from Facebook Developer page : developers.facebook.com
'''This access token expires every two hours for security reasons but this can be overcome by using an extended access token. The one used below is an extended token
and is valid till November 7th 2017. This is a reference to the API.'''
graph = facebook.GraphAPI(access_token="EAABpaWOJYT8BALCrZBXNm6ZAGYZBPiJ7qxpEnMYWK0XZB1I7AbHQ5tfmZBnqhHKg2kAtUk9CV0ianlZBnPwWxpgtJ5mIZB9Jb6u17dHvMDRA3H8yfqX5ON1LRpxo9ZAnR5Xv9lAepH2Ohx338ZBjiO47IqpXlV8lvkY1o9UzFVaDQWQZDZD", version = "2.7")

# initializing states for event choice, not really used yet
CHOOSE_EVENT_CATEGORY = 0
CHOSEN_EVENT_CATEGORY = 1


class EveBot(telepot.helper.ChatHandler):

    def __init__(self, *args, **kwargs):
        super(EveBot, self).__init__(include_callback_query=True, *args, **kwargs)
        self.state = CHOOSE_EVENT_CATEGORY
        self.event_category = None

    def on_chat_message(self, msg):
        global cat_bot
        content_type, chat_type, chat_id = telepot.glance(msg)

        # default response 
        response = '''Hi!! I\'m Eve, the event bot. I will show you the most happening events at NTU from your favorite clubs
                      Please enter /events to display the categories of the events. '''

        # handle only messages with text content
        if content_type == 'text':

            # get message payload
            msg_text = msg['text']


            if (msg_text.startswith('/')):

                # parse the command excluding the '/' (from TGIF)
                command = msg_text[1:].lower()

                # interpret the commands and provide response accordingly
                if (self.state == CHOOSE_EVENT_CATEGORY and command == 'events'):

                    # get available event categories
                    event_categories = ('Technology', 'Culture', 'Music', 'Dance', 'Sports', 'Miscellaneous')

                    # custom keyboard
                    event_categories_keyboard = ReplyKeyboardMarkup(one_time_keyboard=True, keyboard=[
                        [KeyboardButton(text=event_category)] for event_category in event_categories
                    ] + [[KeyboardButton(text='Nevermind')]])

                    response = 'Please selecct the category from which you would like to see events.'
                    bot.sendMessage(chat_id, response, reply_markup=event_categories_keyboard)
                    self.state == CHOSEN_EVENT_CATEGORY
                    # this somehow stops the bot from sending the response twice
                    return

   
            if (msg_text == 'Technology'):
                database_events = database['database_events_tech']
            elif (msg_text == 'Culture'):
                database_events = database['database_events_culture']
            elif (msg_text == 'Music'):
                database_events = database['database_events_music']
            elif (msg_text == 'Dance'):
                database_events = database['database_events_dance']
            elif (msg_text == 'Sports'):
                database_events = database['database_events_sports']
            elif (msg_text == 'Miscellaneous'):
                database_events = database['database_events_misc']
    
            
            for i in range(len(database_events)):        # for loop used to parse over the elements of the list
                    
                 # API call is made to search for events in the list database_events_tech

                events = graph.search(type='event',q=[database_events[i]])
                for event in events['data']:
                    #Result obtained is stored in a list
                    response = (event['name'] + event['description'])
                    print ('event_id: ', event['id'])
                    bot.sendMessage(chat_id, response)

        else:
                # response = 'Please choose an event category!'
            pass

        # send the response
        bot.sendMessage(chat_id, response)


    def on_callback_query(msg):
        global cat_bot
        query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')

        # answer callback query or else telegram will forever wait on this
        bot.answerCallbackQuery(query_id)


bot = DelegatorBot(TOKEN, [
    pave_event_space()
    (per_chat_id(), create_open, EveBot, timeout=100)
])
MessageLoop(bot).run_as_thread()

# show in cmd that bot is running
bot_name = bot.getMe()['first_name']
print(bot_name + ' is running...')

while True:
    time.sleep(10)
