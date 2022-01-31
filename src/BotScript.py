#!/usr/bin/python3
"""Twitter-Bot Script.

Includes multiprocessing to handle
different twets while computing.

Artificial Creativity
CIS - LMU Munich
Philipp Wicke, PhD

Authors:
    Miha Kacicnik
    Philipp Koch

2022
"""


from dotenv import load_dotenv, find_dotenv
from RapMachineBackendGPT2 import RapMachineGPT2
from multiprocessing import Process, Queue
from tweepy.streaming import Stream

import fasttext
import json
import logging
import os
import re
import sys
import time
import tweepy

logging.basicConfig(filename='BotScript.log', level=logging.INFO)

MODEL_STR: str = '.model/GPT2-2Ep'
SLURLIST_STR: str = 'OffWords.txt'
DONE: str = 'DONE'
TWITTER_NAME: str = 'RapMachine7'

# Load Credentials
load_dotenv(find_dotenv())
CONSUMER_API_KEY: str = os.environ.get(
    "CONSUMER_API_KEY", None)
CONSUMER_API_KEY_SECRET: str = os.environ.get(
    "CONSUMER_API_KEY_SECRET", None)
ACCESS_TOKEN: str = os.environ.get(
    "ACCESS_TOKEN", None)
ACCESS_TOKEN_SECRET: str = os.environ.get(
    "ACCESS_TOKEN_SECRET", None)

# Connect to Twitter API
authenticator = tweepy.OAuth1UserHandler(
    CONSUMER_API_KEY,
    CONSUMER_API_KEY_SECRET)
authenticator.set_access_token(
    ACCESS_TOKEN,
    ACCESS_TOKEN_SECRET)
api = tweepy.API(
    authenticator,
    wait_on_rate_limit=True)

fmodel = fasttext.load_model('lid.176.bin')


def queuer(q_q_w, q_w_q):
    """Stream tweets and transfer to worker."""
    global WORKER
    WORKER = True  # Worker variable

    class CustomStream(Stream):

        def __init__(self, cap, caps, at, ats):
            super().__init__(cap, caps, at, ats)

        def on_data(self, raw_data):
            logging.info('Tweet detected.')
            data: dict = json.loads(raw_data)

            if 'text' not in data.keys():
                return super().on_data(raw_data)
            else:
                user, text, tweet_id = (
                    data['user']['screen_name'],
                    data['text'],
                    data['id'])

                text = re.sub(r'(\s*@' + TWITTER_NAME + '\s*)', '', text)
                logging.info(
                    ('Received a tweet: ' + str(user) + " " + str(text)))
                print('RECEIVED:', str(text))

                res = fmodel.predict(text)[0][0]
                if res != '__label__en':
                    print('Tweet not english')
                    api.update_status(
                        ('@' + str(user) + ' Tweet must be in english.'),
                        in_reply_to_status_id=str(tweet_id),
                        auto_populate_reply_metadata=True)
                    return super().on_data(raw_data)

                # Check if worker is available
                global WORKER
                if WORKER:
                    WORKER = False
                    q_q_w.put((user, text, tweet_id))

                else:
                    if not q_w_q.empty():
                        if q_w_q.get() == DONE:
                            WORKER = True
                        else:
                            raise Exception((
                                "ERROR:\n\t'-> This state mustn't be reached."
                                "queue non empty and state-variable True"))
                    else:
                        try:
                            msg: str = RapMachine(
                                MODEL_STR).working_msg(user)
                            logging.info(('Worker unavailable: ' + str(msg)))
                            api.update_status(
                                msg,
                                in_reply_to_status_id=str(tweet_id),
                                auto_populate_reply_metadata=True)
                        except Exception as e:
                            logging.error(e)

                return super().on_data(raw_data)

    # Init Listener
    listener = CustomStream(
            CONSUMER_API_KEY,
            CONSUMER_API_KEY_SECRET,
            ACCESS_TOKEN,
            ACCESS_TOKEN_SECRET,
            )

    # Loop and reconnect exponentially
    exp_counter = 1
    while True:
        if exp_counter > 300:
            exp_counter = 1
        else:
            time.sleep(exp_counter)
            exp_counter = exp_counter ** 2
        try:
            # DO NOT CHANGE TRACK, OTHERWISE SPAM WILL HAPPEN
            listener.filter(track=[TWITTER_NAME])
        except Exception as e:
            exp_counter = 1
            logging.error((ERROR % "Trying to reconnect..."))


def worker(q_q_w, q_w_q):
    """Handle language generation."""
    while True:
        if not q_q_w.empty():
            user, text, tweet_id = q_q_w.get()

            rmb: RapMachine = RapMachineGPT2(
                MODEL_STR,
                SLURLIST_STR)
            rmb.load()
            logging.info('load backend')
            input_str: str = '@' + user + " " + text
            generated = rmb.generate(
                input_str, 4)

            # TODO
            ranked: list = rmb.rank(generated)
            censored: str = rmb.censor(ranked[0])

            logging.info('About to send: ' + censored)
            try:
                api.update_status(
                    censored,
                    in_reply_to_status_id=str(tweet_id),
                    auto_populate_reply_metadata=True)
            except Exception as e:
                logging.error(e)
            q_w_q.put(DONE)
        else:
            time.sleep(1)


if __name__ == '__main__':
    q_q_w = Queue()
    q_w_q = Queue()
    p0 = Process(target=queuer, args=(q_q_w, q_w_q,))
    p1 = Process(target=worker, args=(q_q_w, q_w_q,))
    p0.start()
    p1.start()
