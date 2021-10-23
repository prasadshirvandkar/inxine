import tweepy


class Twitter:
    def __init__(self):
        self.auth = tweepy.OAuthHandler(
            "H43NnEVDF28PPoBetXxzFcEJd", "Qe8NKqtF9zMtCS8HU4C1UjtYCeCTBExE2rWQyznBOe641d8xBb")
        self.auth.set_access_token("373839213-FZs4kUvi1kyjPPkAanhKBBv0KiaP7SeKgRH4CrVZ",
                                   "UFILHVcRYgpQkCl3VtZbDTJmK1AupUv5s4IOMfXOlFOj4")
        self.api = tweepy.API(
            self.auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    def sample_call(self):
        vaccine_text_query_en = "कोविड -filter:retweets AND -filter:replies"
        vaccineTweetList = list()
        enTweets = tweepy.Cursor(self.api.search, q=vaccine_text_query_en, lang='hi', tweet_mode="extended").items(
            1)
        for tweet in enTweets:
            vaccineTweetList.append(tweet._json)

        return vaccineTweetList

    def _meet_basic_tweet_requirements(self):
        '''
        Add basic tweet requirements logic, like language, country, covid type etc.
        :return: boolean
        '''
        vaccine_keywords_en = 'covid,vaccine'.replace(",", " OR ")
        print(len(vaccine_keywords_en.split(' OR ')))

        vaccineTweetList = list()
        keywords_split_en = vaccine_keywords_en.split(' OR ')
        for word in keywords_split_en:
            vaccine_text_query_en = word + " -filter:retweets AND -filter:replies"
            enTweets = tweepy.Cursor(self.api.search, q=vaccine_text_query_en, count=100, lang='en',
                                     tweet_mode="extended").items(
                2)
            for tweet in enTweets:
                vaccineTweetList.append(tweet._json)

    def get_tweets_by_poi_screen_name(self, poi_name):
        '''
        Use user_timeline api to fetch POI related tweets, some postprocessing may be required.
        :return: List
        '''
        poiTweetList = list()
        poi_tweets = tweepy.Cursor(self.api.user_timeline, screen_name=poi_name, count=200, exclude_replies=True,
                                   include_rts=False, tweet_mode="extended").items(50)
        for tweet in poi_tweets:
            poiTweetList.append(tweet._json)

        return poiTweetList

    def get_tweets_by_lang_and_keyword(self, vaccine_text_query, query_lang):
        '''
        Use search api to fetch keywords and language related tweets, use tweepy Cursor.
        :return: List
        '''
        vaccineTweetList = list()
        enTweets = tweepy.Cursor(self.api.search, q=vaccine_text_query, lang=query_lang, tweet_mode="extended").items(
            1072)
        for tweet in enTweets:
            vaccineTweetList.append(tweet._json)

        return vaccineTweetList

    def get_tweets_by_lang_and_keyword_alt(self, vaccine_text_query, query_lang):
        '''
        Use search api to fetch keywords and language related tweets, use tweepy Cursor.
        :return: List
        '''
        vaccineTweetList = list()
        enTweets = tweepy.Cursor(self.api.search, q=vaccine_text_query, lang=query_lang, count=100,
                                 tweet_mode="extended").pages(2)
        for page in enTweets:
            for tweet in page:
                vaccineTweetList.append(tweet._json)

        return vaccineTweetList

    def get_tweets_by_poi(self, poi_name):
        poiTweetList = list()
        pages = tweepy.Cursor(self.api.user_timeline, id=poi_name, count=190, exclude_replies=True,
                              include_rts=False, tweet_mode="extended").pages(30)
        for page in pages:
            for tweet in page:
                poiTweetList.append(tweet._json)

        return poiTweetList

    def get_replies(self, conversation_id):
        '''
        Get replies for a particular tweet_id, use max_id and since_id.
        For more info: https://developer.twitter.com/en/docs/twitter-api/v1/tweets/timelines/guides/working-with-timelines
        :return: List
        '''
        # conversationId = ' OR '.join([conversation for conversation in conversation_ids])
        text_query = f"conversation_id:{conversation_id}"
        lang = 'en OR hi OR es'

        repliesTweets = tweepy.Cursor(self.api.search, q=text_query, lang=lang, tweet_mode="extended").items(200)
        tweetRepliesList = list()
        for tweet in repliesTweets:
            tweetRepliesList.append(tweet._json)

        return tweetRepliesList

    def get_replies_alternative(self, username):
        '''
        Get replies for a particular tweet_id, use max_id and since_id.
        For more info: https://developer.twitter.com/en/docs/twitter-api/v1/tweets/timelines/guides/working-with-timelines
        :return: List
        '''
        # conversationId = ' OR '.join([conversation for conversation in conversation_ids])
        text_query = f"to:{username} -filter:links filter:replies"
        lang = 'en OR hi'

        repliesTweets = tweepy.Cursor(self.api.search, q=text_query, lang=lang, count=180, tweet_mode="extended").pages(
            35)
        tweetRepliesList = list()
        for page in repliesTweets:
            for tweet in page:
                tweetRepliesList.append(tweet._json)

        return tweetRepliesList

    def get_replies_alternativealt(self, keyword, username):
        '''
        Get replies for a particular tweet_id, use max_id and since_id.
        For more info: https://developer.twitter.com/en/docs/twitter-api/v1/tweets/timelines/guides/working-with-timelines
        :return: List
        '''
        # conversationId = ' OR '.join([conversation for conversation in conversation_ids])
        text_query = f"{keyword} to:{username} -filter:links filter:replies"
        print(f"Query: {text_query}")
        lang = 'en OR hi'

        repliesTweets = tweepy.Cursor(self.api.search, q=text_query, lang=lang, count=180, tweet_mode="extended").pages(35)
        tweetRepliesList = list()
        for page in repliesTweets:
            for tweet in page:
                tweetRepliesList.append(tweet._json)

        return tweetRepliesList


if __name__ == "__main__":
    vaccine_keywords_en_full = 'vaccine mandate,covidvaccine,vaccines,vaccination,vaccine efficacy,booster shot,hydroxychloroquine,covishield,vaccine,antibody,immunity,vaccination drive,covaxin,fullyvaccinated,vaccine hesitancy,seconddose,shots,vaccinate,clinical trials,vaccinessavelives,vaccinated,antibodies,vaccineshortage,covidvaccination,vaccine,vaccinessavelives,jab,pfizer,injection,sputnik,side effects,cowin'
    vaccine_keywords_es = 'anticuerpos,eficacia de la vacuna,vacuna covid,campaña de vacunación,completamente vacunado,vacuna para el covid-19,la inmunidad de grupo,segunda dosis,inyección de refuerzo,dosis de vacuna,efectos secundarios de la vacuna,mandato de vacuna,completamente vacunado,efectos secundarios,vacunado,vacunaton,vacunarse'
    vaccine_keywords_hin = 'कोविशील्ड,खुराक,टीकाकरण अभियान,कोवेक्सिन,रोग प्रतिरोधक शक्ति,वैक्सीन,टीकाकरण,वैक्सीन के साइड इफेक्ट,वाइरस,लसीकरण,दुष्प्रभाव,एस्ट्राजेनेका,खराब असर,कोविड का टीका,एंटीबॉडी,फाइजर,कोविन,कोविड टीका,वैक्सीनेशन,पूर्ण टीकाकरण,वैक्सीन पासपोर्ट,टीका लगवाएं,प्रभाव,टीके,पहली खुराक'
    print(', '.join(f'"{w}"' for w in vaccine_keywords_en_full.split(',')))
    print()
    print(', '.join(f'"{w}"' for w in vaccine_keywords_es.split(',')))
    print()
    print(', '.join(f'"{w}"' for w in vaccine_keywords_hin.split(',')))
    print()
    covid_keywords_en = 'covid,quarantine,breakthechain,oxygen,fullyvaccinated,sarscov2,hospital,pandemic,delta variant,lockdown,virus,ventilator,mask,socialdistancing,remdisivir,cases,corona virus,sanitize,symptoms,staysafe,outbreak,workfromhome,covid-19'
    covid_keywords_es = 'quarentena,cierredeemergencia,autoaislamiento,sintomas,pandemia de covid-19,brote,asintomático,oxígeno,desinfectar,quedateencasa,susanadistancia,autocuarentena,contagios,fiebre,propagación en la comunidad,confinamiento,hospitalización,mascarilla,aislamiento,enfermedad,infección,cilindro de oxígeno'
    covid_keywords_hi = 'वैश्विकमहामारी,सुरक्षित रहें,मास्क,डेल्टा संस्करण,टीकाकरण,अस्पताल,कोविड 19,वेंटिलेटर,वाइरस,कोरोना,संक्रमण,सामाजिक दूरी,ऑक्सीजन,महामारी,कोरोनावाइरस,एंटीबॉडी,सामाजिक दूरी,लॉकडाउन,लक्षण,संगरोध,स्पर्शोन्मुख,दूसरी लहर'
    print(', '.join(f'"{w}"' for w in covid_keywords_en.split(',')))
    print()
    print(', '.join(f'"{w}"' for w in covid_keywords_es.split(',')))
    print()
    print(', '.join(f'"{w}"' for w in covid_keywords_hi.split(',')))
    print()
