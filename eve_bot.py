import urllib
import time, sys
import telepot, facebook, requests
from telepot.loop import MessageLoop
from events_database import database
from telepot import DelegatorBot
from telepot.delegate import pave_event_space, per_chat_id, create_open
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton

with open('.\TOKEN.txt', 'r') as token_file:
    TOKEN = token_file.read()

#A user access token from Facebook Developer page : developers.facebook.com
'''This access token expires every two hours for security reasons but this can be overcome by using an extended access token. The one used below is an extended token
and is valid till November 7th 2017 '''
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
        response = 'Hi!! I\'m Eve, the event bot. I will show you the most happening events at NTU from your favorite clubs'

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

            elif (msg_text == ('Technology' or 'Culture' or 'Music' or 'Dance' or 'Sports' or 'Miscellaneous')):
                response = ('Your choice was ' + msg_text)
                bot.sendMessage(chat_id, response)

                if (msg_text == 'Technology'):
                    database_events = database['database_events_tech'][0]
					
					# Alternative code (try this if the current code doesn't work)
					# intermediate_step = database['database_events_tech']
					# database_events = intermediate_step[0]
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
                else:
                    # maybe implement something later on - but this should never be run since the outer if already limits the inputs
                    pass

                for i in range (len(database_events)):                               # for loop used to parse over the elements of the list
                    # API call is made to search for events in the list database_events_tech
                    events = graph.search(type='event',q=[database_events])

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

