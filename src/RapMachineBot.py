"""Twitter-Bot for RapMachine.

Artificial Creativity
CIS - LMU Munich
Philipp Wicke, PhD

Authors:
    Miha Kacicnik
    Philipp Koch

2022
"""

import os
import time
import tweepy

from dotenv import load_dotenv, find_dotenv
from tweepy.streaming import Stream


load_dotenv(find_dotenv())

CONSUMER_API_KEY: str = os.environ.get(
    "CONSUMER_API_KEY", None)
CONSUMER_API_KEY_SECRET: str = os.environ.get(
    "CONSUMER_API_KEY_SECRET", None)
ACCESS_TOKEN: str = os.environ.get(
    "ACCESS_TOKEN", None)
ACCESS_TOKEN_SECRET: str = os.environ.get(
    "ACCESS_TOKEN_SECRET", None)

assert None not in [
    CONSUMER_API_KEY,
    CONSUMER_API_KEY_SECRET,
    ACCESS_TOKEN_SECRET,
    ACCESS_TOKEN], f"ERROR:\n\t'-> Are all keys correctly provided?"


auth = tweepy.AppAuthHandler(
    CONSUMER_API_KEY,
    CONSUMER_API_KEY_SECRET)
api = tweepy.API(auth)

# api.mentions_timeline()


class CustomStream(Stream):
    def on_data(self, raw_data):
        print(raw_data)
        return super().on_data(raw_data)

if '__main__' ==__name__:


    # def signal_handler(sig, frame):
    #     global run
    #     run = False
    #     print('You pressed Ctrl+C!')
    #     db.close()
    #     print('Database connection closed')
    #     sys.exit(0)
    # signal.signal(signal.SIGINT, signal_handler)



    listener = CustomStream(
        CONSUMER_API_KEY,
        CONSUMER_API_KEY_SECRET,
        ACCESS_TOKEN,
        ACCESS_TOKEN_SECRET)

    exp_counter = 1
    run = True

    while run:
        if exp_counter > 300:
            exp_counter = 1
        else:
            time.sleep(exp_counter)
            exp_counter = exp_counter ** 2
        try:
            listener.filter(track=['@RapMachine7'])
        except Exception as e:
            exp_counter = 1
            print(e)
            print("An Error was thrown. Trying to reconnect...")