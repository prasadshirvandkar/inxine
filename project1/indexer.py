import os
import requests
import pysolr
import preprocessor as p

import pandas as pd
import numpy as np
import itertools as it
import spacy
from spacy.lang.hi import Hindi
import regex as re
import demoji

CORE_NAME = "IRF21P1"
AWS_IP = "3.137.190.136"


# [CAUTION] :: Run this script once, i.e. during core creation


def delete_core(core=CORE_NAME):
    print(os.system('sudo -S <<< "pexplorer" solr -c "solr delete -c {core}"'.format(core=core)))


def create_core(core=CORE_NAME):
    print(os.system(
        'sudo -S <<< "pexplorer" solr -c {core} -n data_driven_schema_configs'.format(core=core)))


def do_initial_setup():
    # delete_core()
    create_core()


class Indexer:
    def __init__(self):
        self.solr_url = f'http://{AWS_IP}:8983/solr/'
        self.connection = pysolr.Solr(self.solr_url + CORE_NAME, always_commit=True, timeout=5000000)

    def create_documents(self, docs):
        print(self.connection.add(docs))

    def add_fields(self):
        data = {
            "add-field": [
                {
                    "name": "poi_name",
                    "type": "string",
                    "multiValued": False
                },
                {
                    "name": "poi_id",
                    "type": "plong",
                    "multiValued": False
                },
                {
                    "name": "verified",
                    "type": "boolean",
                    "multiValued": False
                },
                {
                    "name": "country",
                    "type": "string",
                    "multiValued": False
                },
                {
                    "name": "replied_to_tweet_id",
                    "type": "plong",
                    "multiValued": False
                },
                {
                    "name": "replied_to_user_id",
                    "type": "plong",
                    "multiValued": False
                },
                {
                    "name": "reply_text",
                    "type": "text_general",
                    "multiValued": False
                },
                {
                    "name": "tweet_text",
                    "type": "text_general",
                    "multiValued": False
                },
                {
                    "name": "tweet_lang",
                    "type": "string",
                    "multiValued": False
                },
                {
                    "name": "text_en",
                    "type": "text_en",
                    "multiValued": False
                },
                {
                    "name": "text_es",
                    "type": "text_es",
                    "multiValued": False
                },
                {
                    "name": "text_hi",
                    "type": "text_hi",
                    "multiValued": False
                },
                {
                    "name": "hashtags",
                    "type": "strings",
                    "multiValued": True
                },
                {
                    "name": "mentions",
                    "type": "strings",
                    "multiValued": True
                },
                {
                    "name": "tweet_urls",
                    "type": "strings",
                    "multiValued": True
                },
                {
                    "name": "tweet_emoticons",
                    "type": "strings",
                    "multiValued": True
                },
                {
                    "name": "tweet_date",
                    "type": "pdate",
                    "multiValued": False
                }
            ]
        }

        print(requests.post(self.solr_url + CORE_NAME + "/schema", json=data).json())

collection = [
    {
        "verified": True,
        "country": "USA",
        "id": "1235",
        "replied_to_tweet_id": 1234,
        "replied_to_user_id": 1231,
        "reply_text": "Reply Text Dummy 1",
        "tweet_text": "Tweet Text Dummy. Just to test out indexing 111 !!!",
        "tweet_lang": "en",
        "text_es": "campaña de vacunación",
        "tweet_date": "2021-10-10T16:53:45Z"
    },
    {
        "poi_name": "Narendra Modi",
        "poi_id": "narendra123",
        "verified": True,
        "country": "India",
        "id": "123",
        "replied_to_tweet_id": 1234,
        "replied_to_user_id": 1231,
        "reply_text": "Reply Text Dummy",
        "tweet_text": "Tweet Text Dummy. Just to test out indexing !!!",
        "tweet_lang": "en",
        "text_en": "Tweet Text Dummy. Just to test out indexing !!!",
        "hashtags": ["#testing", "#dummy"],
        "mentions": ["@dummy", "@test"],
        "tweet_urls": ["https://www.google.com"],
        "tweet_emoticons": [";)", ":(", ":)", ":D"],
        "tweet_date": "2021-09-10T16:53:45Z"
    }
]

if __name__ == "__main__":
    i = Indexer()
