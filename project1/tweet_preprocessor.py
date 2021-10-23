import datetime
import demoji
import preprocessor
import pandas as pd
import numpy as np
import itertools as it
import spacy
from spacy.lang.hi import Hindi
import regex as re
import demoji


# demoji.download_codes()


def preprocessing_hi(text_hi):
    tweet_hi = []
    nlp_hi = Hindi()
    tokenized_text = nlp_hi(text_hi)

    tokenized_list = []
    for token in tokenized_text:
        tokenized_list.append(token)

    # Filter by Hashtags
    new_tokenized_list = []
    index = 0
    while index < len(tokenized_list):
        if tokenized_list[index].text == '#':
            index += 2
        elif tokenized_list[index].text == "\n":
            index += 1
        else:
            new_tokenized_list.append(tokenized_list[index])
            index += 1

    for token in new_tokenized_list:
        if (token.text != '\n\n'
                and not token.is_space
                and not token.like_email
                and not token.is_digit
                and len(demoji.findall(token.text)) == 0
                and (re.search(r'#\W+', token.text) is None)
                and (re.search(r'@\S+', token.text) is None)
                and (re.search(r'RT+', token.text) is None)
                and not token.like_url):
            tweet_hi.append(token.text)

    tweet = ' '.join([token for token in tweet_hi])
    return tweet


if __name__ == "__main__":
    hi_tweet = "@kpmaurya1 बीजेपी नेता #बीजेपी ने स्वास्थ्य कर्मियों के साथ की मारपीट " \
               "\n बीजेपी नेता ने स्वास्थ्य कर्मियों के साथ की मारपीट #मारपीट #twitter #कर्मियों कर्मियों :) :( :D :o"
    print(f"OG Text: {hi_tweet}")
    cleaned_text = preprocessing_hi(hi_tweet)
    print(f"Cleaned Text: {cleaned_text}")



class TWPreprocessor:
    @classmethod
    def preprocess(cls, tweet, ispoi):
        '''
        Do tweet pre-processing before indexing, make sure all the field data types are in the format as asked in the project doc.
        :param tweet:
        :return: dict
        '''

        tweet_text = tweet['full_text']
        tweet_lang = str(tweet['lang']).lower()

        preprocessed_text, emojis = _text_cleaner(tweet_text, tweet_lang)

        preprocessed_tweet = {'verified': tweet['user']['verified'], 'country': get_country(tweet_lang),
                              'id': tweet['id_str']}

        if tweet['in_reply_to_status_id'] is not None:
            preprocessed_tweet['replied_to_tweet_id'] = tweet['in_reply_to_status_id']
            preprocessed_tweet['reply_text'] = preprocessed_text

        if tweet['in_reply_to_user_id'] is not None:
            preprocessed_tweet['replied_to_user_id'] = tweet['in_reply_to_user_id']

        preprocessed_tweet['tweet_text'] = tweet['full_text']
        preprocessed_tweet['tweet_lang'] = tweet_lang

        if tweet_lang == 'hi':
            preprocessed_tweet['text_hi'] = preprocessed_text
        elif tweet_lang == 'es':
            preprocessed_tweet['text_es'] = preprocessed_text
        else:
            preprocessed_tweet['text_en'] = preprocessed_text

        if len(tweet['entities']['hashtags']) != 0:
            hashtags = []
            t_hashtags = tweet['entities']['hashtags']
            for hashtag in t_hashtags:
                hashtags.append(hashtag['text'])

            if len(hashtags) not in []:
                preprocessed_tweet['hashtags'] = hashtags

        if len(tweet['entities']['user_mentions']) != 0:
            mentions = []
            t_mentions = tweet['entities']['user_mentions']
            for mention in t_mentions:
                mentions.append(mention['screen_name'])

            if len(mentions) not in []:
                preprocessed_tweet['mentions'] = mentions

        if len(tweet['entities']['urls']) != 0:
            urls = []
            t_urls = tweet['entities']['urls']
            for url in t_urls:
                urls.append(url['url'])

            if len(urls) not in []:
                preprocessed_tweet['tweet_urls'] = urls

        preprocessed_tweet['tweet_emoticons'] = emojis
        preprocessed_tweet['tweet_date'] = str(_get_tweet_date(tweet['created_at']))

        if ispoi:
            preprocessed_tweet['poi_id'] = tweet['user']['id']
            preprocessed_tweet['poi_name'] = tweet['user']['name']
            preprocessed_tweet['country'] = tweet['user']['location']

        return preprocessed_tweet


def get_country(lang):
    country = 'USA'
    if lang == 'hi':
        country = 'India'
    elif lang == 'es':
        country = "Mexico"
    return country


def _get_entities(tweet, type=None):
    result = []
    if type == 'hashtags':
        hashtags = tweet['entities']['hashtags']

        for hashtag in hashtags:
            result.append(hashtag['text'])
    elif type == 'mentions':
        mentions = tweet['entities']['user_mentions']

        for mention in mentions:
            result.append(mention['screen_name'])
    elif type == 'urls':
        urls = tweet['entities']['urls']

        for url in urls:
            result.append(url['url'])

    return result


def _text_cleaner(text, tweet_lang):
    emoticons_happy = list([
        ':-)', ':)', ';)', ':o)', ':]', ':3', ':c)', ':>', '=]', '8)', '=)', ':}',
        ':^)', ':-D', ':D', '8-D', '8D', 'x-D', 'xD', 'X-D', 'XD', '=-D', '=D',
        '=-3', '=3', ':-))', ":'-)", ":')", ':*', ':^*', '>:P', ':-P', ':P', 'X-P',
        'x-p', 'xp', 'XP', ':-p', ':p', '=p', ':-b', ':b', '>:)', '>;)', '>:-)',
        '<3'
    ])
    emoticons_sad = list([
        ':L', ':-/', '>:/', ':S', '>:[', ':@', ':-(', ':[', ':-||', '=L', ':<',
        ':-[', ':-<', '=\\', '=/', '>:(', ':(', '>.<', ":'-(", ":'(", ':\\', ':-c',
        ':c', ':{', '>:\\', ';('
    ])
    all_emoticons = emoticons_happy + emoticons_sad

    emojis = list(demoji.findall(text).keys())
    clean_text = demoji.replace(text, '')

    for emo in all_emoticons:
        if emo in clean_text:
            clean_text = clean_text.replace(emo, '')
            emojis.append(emo)

    clean_text = preprocessing_hi(text) if tweet_lang == 'hi' else preprocessor.clean(text)
    # preprocessor.set_options(preprocessor.OPT.EMOJI, preprocessor.OPT.SMILEY)
    # emojis= preprocessor.parse(text)

    return clean_text, emojis


def _get_tweet_date(tweet_date):
    return _hour_rounder(datetime.datetime.strptime(tweet_date, '%a %b %d %H:%M:%S +0000 %Y'))


def _hour_rounder(t):
    # Rounds to nearest hour by adding a timedelta hour if minute >= 30
    return (t.replace(second=0, microsecond=0, minute=0, hour=t.hour)
            + datetime.timedelta(hours=t.minute // 30))
