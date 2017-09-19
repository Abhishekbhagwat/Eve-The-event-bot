#This code is written by Abhishek Bhagwat. Please give credits to the author if this repository is cloned and used. Find this author on GitHub : github.com/Abhishekbhagwat

#Eve : The Event Bot

#This bot is built to scrape upcoming events data from facebook pages of clubs at NTU and display them accprding to the user's preference


#This bot uses Facebook's Graph API to make a request and then displays the event 



import facebook     #Facebook module is imported to access the GraphAPI to make API calls
import requests     #requests module is imported to make requests to the server to send and recieve the data
import sys


#A user access token from Facebook Developer page : developers.facebook.com


'''This access token expires every two hours for security reasons but this can be overcome by using an extended access token. The one used below is an extended token 
and is valid till November 7th 2017 '''


graph = facebook.GraphAPI(access_token="EAABpaWOJYT8BALCrZBXNm6ZAGYZBPiJ7qxpEnMYWK0XZB1I7AbHQ5tfmZBnqhHKg2kAtUk9CV0ianlZBnPwWxpgtJ5mIZB9Jb6u17dHvMDRA3H8yfqX5ON1LRpxo9ZAnR5Xv9lAepH2Ohx338ZBjiO47IqpXlV8lvkY1o9UzFVaDQWQZDZD", version = "2.7")


#The following code is the welcome code and will introduce the bot and displays the preferences available to chose from

print ("Hi!! I'm Eve, the event bot. I will show you the most happening events at NTU from your favorite clubs")

print("Please selecct the category from which you would like to see events.")

print("""
                1.Technology
                2.Culture
                3.Music         
                4.Dance
                5.Sports
                6.Miscellaneous """)


x = int(input("Please input your choice"))  #Asks the user for input 


print("Your choice is ",x) #User's choice is output



while count!=0:

        if x == 1:   #if the coice is 1 then the following block of address is executed
                print("You have chosen technology as your preference")
                print("The most happening events are")
 

                database_events_tech = ['TGIF Hacks','Web exploitation','iNTUition',] # This list consists of data which is populated by events which are usually held regularly. Only such events are populated due to quality control.


                for i in range (len(database_events_tech)):                               # for loop used to parse over the elements of the list                        
                events = graph.search(type='event',q=[database_events_tech])      #API call is made to search for events in the list database_events_tech


                for event in events['data']:                                            #Result obtained is stored in a list                                           
                        print(event['id'],event['name'],event['description'])           #attributes of the event 'id','name','description' are printed


                process = input(("Do you want to quit ? (y/n)"))


                if process == 'y':
                        count=0
                else:
                        count+=1

        elif x == 2:
                print("You have chosen culture as your preference")
                print("The most happening events are")


                database_events_cult = []


                for i in range (len(database_events_cult)):
                        events = graph.search(type='event',q=[database_events_cult])


                for event in events['data']:
                        print(event['id'],event['name'],event['description'])


                process = input(("Do you want to quit ? (y/n)"))


                if process == 'y':
                        count=0
                else:
                        count+=1



        elif x == 3:
                print("You have chosen Music as your preference")
                print("The most happening events are")



                database_events_mus = []


                for i in range (len(database_events_mus)):
                        events = graph.search(type='event',q=[database_events_mus])


                for event in events['data']:
                        print(event['id'],event['name'],event['description'])


                process = input(("Do you want to quit ? (y/n)"))


                if process == 'y':
                        count=0
                else:
                        count+=1



        elif x == 4:
                print("You have chosen Dance as your preference")
                print("The most happening events are")


                database_events_dan = []


                for i in range (len(database_events_dan)):
                        events = graph.search(type='event',q=[database_events_dan])



                for event in events['data']:
                        print(event['id'],event['name'],event['description'])


                process = input(("Do you want to quit ? (y/n)"))


                if process == 'y':
                        count=0
                else:
                        count+=1



        elif x == 5:
                print("You have chosen sports as your preference")
                print("The most happening events are")


                database_events_spr = []


                for i in range(len(database_events_spr)):
                        events = graph.search(type='event',q=[database_events_spr])


                for event in events['data']:
                        print(event['id'],event['name'],event['description'])


                process = input(("Do you want to quit ? (y/n)"))


                if process == 'y':
                        count=0
                else:
                        count+=1



        elif x == 6:
                print("You have chosen Miscellaneous events as your preference")
                print("The most happening events are")


                database_events_misc = []


                for i in range(len(database_events_misc)):
                        events = graph.search(type='event',q=[database_events_misc])



                for event in events['data']:
                        print(event['id'],event['name'],event['description'])
                

                process = input(("Do you want to quit ? (y/n)"))


                if process == 'y':
                        count=0
                else:
                        count+=1


