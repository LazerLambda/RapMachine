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
from RapMachineBackend import RapMachine
from multiprocessing import Process, Queue
from multiprocessing import shared_memory
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

MODEL_STR: str =\
    '/home/philko/Documents/Uni/WiSe2122/CL/KuenstKrea/RapMachine/.model/T5-1'

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
                user, text = data['user']['screen_name'], data['text']

                text = re.sub(r'(\s*@RapMachine7\s*)', '', text)
                logging.info(
                    ('Received a tweet: ' + str(user) + " " + str(text)))
                print('RECEIVED:', str(text))

                res = fmodel.predict(text)[0][0]
                if res != '__label__en':
                    return super().on_data(raw_data)

                # Check if worker is available
                global WORKER
                if WORKER:
                    WORKER = False
                    q_q_w.put((user, text))

                else:
                    if not q_w_q.empty():
                        if q_w_q.get() == 'DONE':
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
                            api.update_status(msg)
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
            # DO NOT CHANGE TRACK, OTHERWISE SPAM HAPPENS
            listener.filter(track=['RapMachine7'])
        except Exception as e:
            exp_counter = 1
            logging.error((ERROR % "Trying to reconnect..."))


def worker(q_q_w, q_w_q):
    """Handle language generation."""
    while True:
        if not q_q_w.empty():
            user, text = q_q_w.get()

            rmb: RapMachine = RapMachine(
                MODEL_STR)
            rmb.load()
            logging.info('load backend')
            generated = rmb.generate(
                ['compton', 'luck', 'gangsta', 'car', 'police', 'apple'], 4)

            # TODO
            # ranked: list = self.rmb.rank(generated)
            # censored: str = self.rmb.censor(ranked)

            censored = 'TEST-OUTPUT'

            try:
                api.update_status(censored)
            except Exception as e:
                logging.error(e)
            q_w_q.put('DONE')
        else:
            print("Waiting for tweets.")
            time.sleep(1)


if __name__ == '__main__':
    q_q_w = Queue()
    q_w_q = Queue()
    p0 = Process(target=queuer, args=(q_q_w, q_w_q,))
    p1 = Process(target=worker, args=(q_q_w, q_w_q,))
    p0.start()
    p1.start()
