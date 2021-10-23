import json

import pandas as pd

from indexer import Indexer
from tweet_preprocessor import TWPreprocessor
from twitter import Twitter
import time

normal_tweets_collection = False
es_tweets = False
hi_tweets = False

poi_collection_india = False
poi_collection_usa = False
poi_collection_mexico = False

reply_collection_knob = False
reply_collection_poi = True
reply_collection_alt = False
reply_collection_alt_alt = False

def read_config():
    with open("config.json") as json_file:
        data = json.load(json_file)
    return data


def write_config(data):
    with open("config.json", 'w') as json_file:
        json.dump(data, json_file)


def save_file(data, filename):
    df = pd.DataFrame(data)
    df.to_pickle("data/" + filename)


def read_file(filename):
    return pd.read_pickle('data/' + str(filename))


def main():
    indexer = Indexer()
    twitter = Twitter()

    vaccine_keywords_en_full = 'vaccine mandate,covidvaccine,vaccines,vaccination,vaccine efficacy,booster shot,' \
                               'hydroxychloroquine,covishield,vaccine,antibody,immunity,"vaccination drive",covaxin,' \
                               'fullyvaccinated,vaccine hesitancy,seconddose,shots,vaccinate,clinical trials,' \
                               'vaccinessavelives,vaccinated,antibodies,vaccineshortage,covidvaccination,vaccine,' \
                               'vaccinessavelives,jab,pfizer,injection,sputnik,side effects,cowin,covid,quarantine,covid19,breakthechain,oxygen,fullyvaccinated,' \
                               'sarscov2,hospital,covid' \
                               'pandemic,delta variant,lockdown,virus,ventilator,mask,socialdistancing,' \
                               'remdisivir,cases,corona virus,sanitize,symptoms,staysafe,outbreak,workfromhome,covid-19,कोविशील्ड,खुराक,टीकाकरण अभियान,कोवेक्सिन,' \
                               'रोग प्रतिरोधक शक्ति,वैक्सीन,टीकाकरण,वैक्सीन के साइड इफेक्ट,वाइरस,लसीकरण,दुष्प्रभाव,एस्ट्राजेनेका,खराब असर,कोविड का टीका,एंटीबॉडी,फाइजर,कोविन,कोविड टीका,वैक्सीनेशन,पूर्ण टीकाकरण,' \
                               'वैक्सीन पासपोर्ट,टीका लगवाएं,प्रभाव,टीके,पहली खुराक,वैश्विकमहामारी,सुरक्षित रहें,मास्क,डेल्टा संस्करण,टीकाकरण,अस्पताल,कोविड 19,वेंटिलेटर,वाइरस,कोरोना,संक्रमण,सामाजिक दूरी,ऑक्सीजन,' \
                               'महामारी,कोरोनावाइरस,एंटीबॉडी,सामाजिक दूरी,लॉकडाउन,लक्षण,संगरोध,स्पर्शोन्मुख,दूसरी लहर,' \
                               'anticuerpos,eficacia de la vacuna,vacuna covid,campaña de vacunación,completamente vacunado,' \
                               'vacuna para el covid-19,la inmunidad de grupo,segunda dosis,inyección de refuerzo,dosis de vacuna,' \
                               'efectos secundarios de la vacuna,mandato de vacuna,completamente vacunado,efectos secundarios,vacunado,' \
                               'vacunaton,vacunarse,quarentena,cierredeemergencia,autoaislamiento,sintomas,pandemia de covid-19,' \
                               'brote,asintomático,oxígeno,desinfectar,quedateencasa,susanadistancia,autocuarentena,contagios,fiebre,' \
                               'propagación en la comunidad,confinamiento,hospitalización,mascarilla,aislamiento,enfermedad,infección,' \
                               'cilindro de oxígeno,covid'.replace(",", " OR ")

    vaccine_keywords_en_full_list = vaccine_keywords_en_full.split(' OR ')

    if normal_tweets_collection:
        vaccine_keywords_en = 'immunity,vaccinate,antibodies,vaccineshortage,covidvaccination,vaccine,vaccinessavelives,vaccineshortage,jab,pfizer,injection,sputnik,"side effects",cowin'.replace(
            ",", " OR ")
        keywords_split_en = vaccine_keywords_en.split(' OR ')

        for word in keywords_split_en:
            print(f"Getting Tweets for: {word} ...")
            vaccine_text_query_en = word + " -filter:retweets AND -filter:replies"
            start_time = time.time()
            raw_tweets = twitter.get_tweets_by_lang_and_keyword_alt(vaccine_text_query_en, 'en')
            print(f"--- Took %s seconds for {word} ---" % (time.time() - start_time))
            print(f"Retrieved {len(raw_tweets)} for {word}")
            processed_tweets = []
            for tw in raw_tweets:
                processed_tweets.append(TWPreprocessor.preprocess(tw, False))

            indexer.create_documents(processed_tweets)
            save_file(processed_tweets, f"'en_keywords_{word}_2.pkl',")

            print(f"Processing and Indexing Done for {word}")

        print("English Words Done")

    if es_tweets:
        # vaccine_keywords_es = 'anticuerpos,"eficacia de la vacuna","vacuna covid","campaña de vacunación","completamente vacunado","vacuna para el covid-19","la inmunidad de grupo","segunda dosis","inyección de refuerzo","dosis de vacuna","efectos secundarios de la vacuna","mandato de vacuna","completamente vacunado","efectos secundarios",vacunado,vacunaton,vacunarse'.replace(
        #   ",", " OR ")
        vaccine_keywords_es = '"vacuna covid","efectos secundarios de la vacuna","mandato de vacuna","completamente vacunado","efectos secundarios",vacunado,vacunaton,vacunarse'.replace(
            ",", " OR ")
        keywords_split_es = vaccine_keywords_es.split(' OR ')

        for word in keywords_split_es:
            print(f"Getting Tweets for: {word} ...")
            vaccine_text_query_en = word + " -filter:retweets AND -filter:replies"
            start_time = time.time()
            raw_tweets = twitter.get_tweets_by_lang_and_keyword_alt(vaccine_text_query_en, 'es')
            print(f"--- Took %s seconds for {word} ---" % (time.time() - start_time))
            print(f"Retrieved {len(raw_tweets)} for {word}")
            processed_tweets = []
            for tw in raw_tweets:
                processed_tweets.append(TWPreprocessor.preprocess(tw, False))

            indexer.create_documents(processed_tweets)
            save_file(processed_tweets, f"es_keywords_{word}.pkl',")
            print('Indexing and Saving Done for { ' + word + ' }')

        print("Spanish Words Done")

    # vaccine_keywords_hin = 'कोविशील्ड,खुराक,"टीकाकरण अभियान",कोवेक्सिन,"रोग प्रतिरोधक शक्ति",वैक्सीन,टीकाकरण,"वैक्सीन के साइड इफेक्ट",वाइरस,लसीकरण,दुष्प्रभाव,एस्ट्राजेनेका,"खराब असर","कोविड का टीका",एंटीबॉडी,फाइजर,कोविन,"कोविड टीका",वैक्सीनेशन,"पूर्ण टीकाकरण","वैक्सीन पासपोर्ट","टीका लगवाएं",प्रभाव,टीके,"पहली खुराक"'.replace(
    # ",", " OR ")

    if hi_tweets:
        vaccine_keywords_hin = 'कोवेक्सिन,कोविशील्ड,लसीकरण,"रोग प्रतिरोधक शक्ति",वैक्सीन,टीकाकरण,"वैक्सीन के साइड इफेक्ट",वाइरस,लसीकरण,दुष्प्रभाव,एस्ट्राजेनेका,"खराब असर","कोविड का टीका",एंटीबॉडी,फाइजर'.replace(
            ",", " OR ")
        keywords_split_hin = vaccine_keywords_hin.split(' OR ')

        for word in keywords_split_hin:
            print(f"Getting Tweets for: {word} ...")
            vaccine_text_query_en = word + " -filter:retweets AND -filter:replies"
            start_time = time.time()
            raw_tweets = twitter.get_tweets_by_lang_and_keyword_alt(vaccine_text_query_en, 'hi')
            print(f"--- Took %s seconds for {word} ---" % (time.time() - start_time))
            print(f"Retrieved {len(raw_tweets)} for {word}")

            processed_tweets = []
            for tw in raw_tweets:
                processed_tweets.append(TWPreprocessor.preprocess(tw, False))

            indexer.create_documents(processed_tweets)
            save_file(processed_tweets, f"hi_keywords_{word}.pkl',")
            print('Indexing and Saving Done for { ' + word + ' }')

            print("Hindi Words Done")

    # indian_pois = ['narendramodi', 'MoHFW_INDIA', 'smritiirani', 'RahulGandhi', 'rashtrapatibhvn', 'mansukhmandviya', ]
    # us_pois = ['JoeBiden', 'BarackObama', 'KamalaHarris', 'LeaderMcConnell', 'HillaryClinton', 'CDCgov']
    # mexico_pois = ['lopezobrador_', 'JaimeRdzNL', 'RicardoAnayaC', 'FelipeCalderon', 'SSalud_mx']

    if poi_collection_india:
        indian_pois = ['narendramodi', 'MoHFW_INDIA', 'smritiirani', 'RahulGandhi', 'rashtrapatibhvn',
                       'mansukhmandviya']
        for poi in indian_pois:
            print(f"Getting Tweets for: {poi} ...")
            start_time = time.time()
            raw_tweets = twitter.get_tweets_by_poi(poi)
            print(f"--- Took %s seconds for {poi} ---" % (time.time() - start_time))
            print(f"Retrieved {len(raw_tweets)} for {poi}")

            filtered_tweets = []
            for vaccine in vaccine_keywords_en_full_list:
                for tweet in raw_tweets:
                    if vaccine in tweet['full_text']:
                        filtered_tweets.append(tweet)

            print(f"Filtered Tweets: {len(filtered_tweets)}")

            fids = []
            for ftweet in filtered_tweets:
                fids.append(ftweet['id_str'])
            # print(','.join([fid for fid in fids]))
            save_file(fids, f"indian_poi_covid_ids_{poi}.pkl")

            processed_tweets = []
            for tw in filtered_tweets:
                processed_tweets.append(TWPreprocessor.preprocess(tw, True))

            indexer.create_documents(processed_tweets)
            save_file(processed_tweets, f"india_poi_covid_{poi}.pkl,")

            print('Indexing and Saving Done for { ' + poi + ' }')
        print("Indian POI Done")

    if poi_collection_usa:
        us_pois = ['JoeBiden', 'BarackObama', 'KamalaHarris', 'LeaderMcConnell', 'HillaryClinton', 'CDCgov']
        for poi in us_pois:
            print(f"Getting Tweets for: {poi} ...")
            start_time = time.time()
            raw_tweets = twitter.get_tweets_by_poi(poi)
            print(f"--- Took %s seconds for {poi} ---" % (time.time() - start_time))
            print(f"Retrieved {len(raw_tweets)} for {poi}")

            filtered_tweets = []
            for vaccine in vaccine_keywords_en_full_list:
                for tweet in raw_tweets:
                    if vaccine in tweet['full_text']:
                        filtered_tweets.append(tweet)

            print(f"Filtered Tweets: {len(filtered_tweets)}")

            fids = []
            for ftweet in filtered_tweets:
                fids.append(ftweet['id_str'])
            # print(','.join([fid for fid in fids]))
            save_file(fids, f"us_poi_covid_ids_{poi}.pkl")

            processed_tweets = []
            for tw in filtered_tweets:
                processed_tweets.append(TWPreprocessor.preprocess(tw, True))

            indexer.create_documents(processed_tweets)
            save_file(processed_tweets, f"us_poi_covid_{poi}.pkl,")

            print('Indexing and Saving Done for { ' + poi + ' }')
        print("USA POI Done")

    if poi_collection_mexico:
        mexico_pois = ['lopezobrador_', 'JaimeRdzNL', 'RicardoAnayaC', 'FelipeCalderon', 'SSalud_mx']
        for poi in mexico_pois:
            print(f"Getting Tweets for: {poi} ...")
            start_time = time.time()
            raw_tweets = twitter.get_tweets_by_poi(poi)
            print(f"--- Took %s seconds for {poi} ---" % (time.time() - start_time))
            print(f"Retrieved {len(raw_tweets)} for {poi}")

            filtered_tweets = []
            for vaccine in vaccine_keywords_en_full_list:
                for tweet in raw_tweets:
                    if vaccine in tweet['full_text']:
                        filtered_tweets.append(tweet)

            print(f"Filtered Tweets: {len(filtered_tweets)}")

            fids = []
            for ftweet in filtered_tweets:
                fids.append(ftweet['id_str'])
            # print(','.join([fid for fid in fids]))
            save_file(fids, f"mexico_poi_covid_ids_{poi}.pkl")

            processed_tweets = []
            for tw in filtered_tweets:
                processed_tweets.append(TWPreprocessor.preprocess(tw, True))

            indexer.create_documents(processed_tweets)
            save_file(processed_tweets, f"mexico_poi_covid_{poi}.pkl,")

            print('Indexing and Saving Done for { ' + poi + ' }')
        print("Mexico POI Done")

    if reply_collection_knob:
        # Write a driver logic for reply collection, use the tweets from the data files for which the replies are to collected.
        enFiles = []

        tweets_received = []
        for file in enFiles:
            ids = read_file(file)['id']
            for _id in ids:
                print(f"Getting Tweets for: {file} with Conversation ID: {id} ...")
                start_time = time.time()
                raw_tweets = twitter.get_replies(_id)
                print(f"--- Took %s seconds for {file} ---" % (time.time() - start_time))
                print(f"Retrieved {len(raw_tweets)} for {file}")

                if len(raw_tweets) != 0:
                    processed_tweets = []
                    for tw in raw_tweets:
                        processed_tweets.append(TWPreprocessor.preprocess(tw, False))

                    indexer.create_documents(processed_tweets)
                    print('Indexing and Saving Done')

        print("Total Received: " + str(len(tweets_received)))

    if reply_collection_poi:
        # Write a driver logic for reply collection, use the tweets from the data files for which the replies are to collected.
        enFiles = [
            #'us_poi_covid_ids_HillaryClinton.pkl',
            'us_poi_covid_ids_KamalaHarris.pkl'
        ]

        tweets_received = []
        count = 0
        for file in enFiles:
            ids = read_file(file).iterrows()
            for _id in ids:
                cid = _id[1][0]
                print(f"Getting Tweets for: {file} with Conversation ID: {cid} ...")
                start_time = time.time()
                raw_tweets = twitter.get_replies(cid)
                print(f"--- Took %s seconds for {file} ---" % (time.time() - start_time))
                print(f"Retrieved {len(raw_tweets)} for {file}")

                if len(raw_tweets) >= 10:
                    count += 1
                    processed_tweets = []
                    for tw in raw_tweets:
                        processed_tweets.append(TWPreprocessor.preprocess(tw, False))

                    indexer.create_documents(processed_tweets)
                    print('Indexing and Saving Done')

        print("Total Received: " + str(len(tweets_received)))

    if reply_collection_alt:
        indian_pois = ['narendramodi', 'MoHFW_INDIA', 'smritiirani', 'RahulGandhi', 'rashtrapatibhvn',
                       'mansukhmandviya']
        for poi in indian_pois:
            print(f"Getting Tweets for: {poi} ...")
            start_time = time.time()
            raw_tweets = twitter.get_replies_alternative(poi)
            print(f"--- Took %s seconds for {poi} ---" % (time.time() - start_time))
            print(f"Retrieved {len(raw_tweets)} for {poi}")

            filtered_tweets = []
            for vaccine in vaccine_keywords_en_full_list:
                for tweet in raw_tweets:
                    if vaccine in tweet['full_text'] and tweet['in_reply_to_status_id'] is not None and tweet[
                        'in_reply_to_user_id'] is not None:
                        filtered_tweets.append(tweet)

            print(f"Filtered Tweets: {len(filtered_tweets)}")

            processed_tweets = []
            for tw in filtered_tweets:
                processed_tweets.append(TWPreprocessor.preprocess(tw, False))

            indexer.create_documents(processed_tweets)
            print('Indexing and Saving Done for { ' + poi + ' }')
        print("POI Done")

    if reply_collection_alt_alt:
        vaccine_keywords_en_full = 'vaccine,vaccines,vaccination,covishield,antibody,immunity,covaxin,fullyvaccinated,vaccinated,antibodies,jab,pfizer,injection,cowin,covid,covid vaccine,quarantine,breakthechain,oxygen,sarscov2,hospital,pandemic,lockdown,virus,ventilator,mask,socialdistancing,cases,corona virus,sanitize,symptoms,staysafe,outbreak,covid-19'
        for keyword in vaccine_keywords_en_full.split(','):
            indian_pois = ['narendramodi', 'MoHFW_INDIA', 'smritiirani', 'RahulGandhi', 'rashtrapatibhvn',
                           'mansukhmandviya']
            us_pois = ['JoeBiden', 'BarackObama', 'KamalaHarris', 'LeaderMcConnell', 'HillaryClinton', 'CDCgov']
            for poi in us_pois:
                print(f"Getting Tweets for: {poi} ...")
                start_time = time.time()
                raw_tweets = twitter.get_replies_alternativealt(keyword, poi)
                print(f"--- Took %s seconds for {poi} ---" % (time.time() - start_time))
                print(f"Retrieved {len(raw_tweets)} for {poi}")

                filtered_tweets = []
                for tweet in raw_tweets:
                    if tweet['in_reply_to_status_id'] is not None and tweet['in_reply_to_user_id'] is not None:
                        filtered_tweets.append(tweet)
                print(f"Filtered Tweets: {len(filtered_tweets)}")

                processed_tweets = []
                for tw in filtered_tweets:
                    processed_tweets.append(TWPreprocessor.preprocess(tw, False))

                indexer.create_documents(processed_tweets)
                print('Indexing and Saving Done for { ' + poi + ' }')


if __name__ == "__main__":
    main()
