import urllib
import time, sys
import telepot, facebook, requests
from telepot.loop import MessageLoop
from events_database import database
from telepot import DelegatorBot
from telepot.delegate import pave_event_space, per_chat_id, create_open
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton

with open('TOKEN.txt', 'r') as token_file:
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

        # handle only messages with text content
        if content_type == 'text':

            # get message payload
            msg_text = msg['text']


            if (msg_text.startswith('/')):

                # parse the command excluding the '/' (from TGIF)
                command = msg_text[1:].lower()

                if (command=="start"):


                # default response
                    response = 'Hi!! I\'m Eve, the event bot. I will show you the most happening events at NTU from your favorite clubs'
                    bot.sendMessage(chat_id,response)

                    bot.sendMessage(chat_id, "Enter the message /events to start")
                    msg_text = msg['text']
                    self.state == CHOSEN_EVENT_CATEGORY

                # allows user to search for a particular event by name, utilizes Facebook's search function
                elif (command.startswith('search')):
                        search_input = msg_text[7:].lower()
                        bot.sendMessage(chat_id, 'You searched for: ' + search_input)

                        print('User searched for ', search_input)

                        events = graph.search(type='event',q=[search_input],limit = 3)
                        for event in events['data']:
                        #Result obtained is stored in a list
                            response = (event['name'] + event['description'])
                            print ('event_id: ', event['id'])
                            bot.sendMessage(chat_id, response)
                        if events['data'] == []:
                            bot.sendMessage(chat_id, 'No results found.')

                # interpret the commands and provide response accordingly
                elif (self.state == CHOOSE_EVENT_CATEGORY and command == 'events'):

                    # get available event categories
                    event_categories = ('Technology', 'Culture', 'Music', 'Dance', 'Sports', 'Miscellaneous')

                    # custom keyboard
                    event_categories_keyboard = ReplyKeyboardMarkup(one_time_keyboard=True, keyboard=[
                        [KeyboardButton(text=event_category)] for event_category in event_categories
                    ] + [[KeyboardButton(text='Nevermind')]])

                    response = 'Please select the category from which you would like to see events.'
                    bot.sendMessage(chat_id, response, reply_markup=event_categories_keyboard)
                    self.state == CHOSEN_EVENT_CATEGORY
                    # this somehow stops the bot from sending the response twice
                    return

                else:
                    bot.sendMessage(chat_id, 'That is not a valid command!')


            elif (msg_text in ('Technology', 'Culture', 'Music', 'Dance', 'Sports', 'Miscellaneous')):
                response = ('Your choice was ' + msg_text)
                bot.sendMessage(chat_id, response)

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
                else:
                    # maybe implement something later on - but this should never be run since the outer if already limits the inputs
                    pass

                for i in database_events:                               # while loop used to parse over the elements of the list
                    # API call is made to search for events in the list database_events_tech
                    events = graph.search(type='event',q=[i],limit = 1)

                    for event in events['data']:
                    #Result obtained is stored in a list
                        response = (event['name'] + event['description'])
                        print ('event_id: ', event['id'])
                        bot.sendMessage(chat_id, response)

            else:
                # response = 'Please choose an event category!'
                bot.sendMessage(chat_id, 'What do you mean?')

        else:
            bot.sendMessage(chat_id, 'I am a text bot! Only text inputs are accepted!')
        # send the response
        #bot.sendMessage(chat_id, response)


    def on_callback_query(msg):
        global cat_bot
        query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')

        # answer callback query or else telegram will forever wait on this
        bot.answerCallbackQuery(query_id)


bot = DelegatorBot(TOKEN, [
    pave_event_space()
    (per_chat_id(), create_open, EveBot, timeout=10000)
])
MessageLoop(bot).run_as_thread()

# show in cmd that bot is running
bot_name = bot.getMe()['first_name']
print(bot_name + ' is running...')

while True:
    time.sleep(10)
