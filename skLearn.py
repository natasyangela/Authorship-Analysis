import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
import tweepy
import csv
import string

def scrapping(username):
    access_token = '528154427-gBB0wjsslCqhSKmpAAOdVabhz8NgrFIrm28eHYKG'
    access_token_secret = 'bEUzJC2b2O40IcBI2K7VA8xDiqvor9bIuoUcuxFnjv4rz'
    api_key = 'ql4wvYMDOEzAayjRthZBazXm7'
    api_secret_key = 'I7dodoD4rouTJOwwP9r6MrsgEHF2YvJ7CsMeYwJwTdNlmjsp2G'

    auth = tweepy.OAuthHandler(api_key, api_secret_key)
    auth.set_access_token(access_token, access_token_secret)
    
    api = tweepy.API(auth)
        
    user_timeline = api.user_timeline(username, count=100, include_rts=False)

    file1=open('DATA_TWEETS.csv','a+',encoding='utf-8')
    writer = csv.writer(file1)
    # writer.writerow(['username','tweets'])
    for tweet in user_timeline:
        idStat = tweet.id_str
        status = api.get_status(idStat,tweet_mode = "extended")
        full_text = status.full_text
        writer.writerow([username,str(full_text.encode('utf-8'))[2:-1]])

    file1.close()

def remove_unwanted_cols(dataset,cols):
    for col in cols:
        del dataset[col]
    return dataset

def tfidf_count():
    data = pd.read_csv('DATA_TWEETS.csv',encoding='iso-8859-9')    

    usernameList = data['username']
    tweets = remove_unwanted_cols(data,['username'])
    # print(len(usernameList.index))
    awal = 0
    akhir =-1
    #awal adalah index awal, akhir adalah pembatas kalo beda username

    # a = ['abc', 'bcd']
    # b = ['haha', 'hhe']
    # a += b
    # print(a)
    for i in range(len(usernameList.index)):  
        if (i == len(usernameList.index)-1 or usernameList[i] != usernameList[i+1] ):
            processed_tweets = ''
            tweetList = []
            username = usernameList[i]
            # print(username)
            awal = akhir +1
            akhir = i
            
            X = tweets.iloc[awal:akhir+1,0].values
            # print(len(X))
            # print(X)
            # print( "awal = " + str(awal))
            # print( "akhir = " + str(akhir))

            # print(X[7]) 
            
            for tweet in range(0, len(X)):  
                # print(X[tweet])
                # Removing hashtag + username
                processed_tweet = re.sub(r'\@\w+|\#','', str(X[tweet]))

                # Removing urls
                processed_tweet = re.sub(r"http\S+|www\S+|https\S+", '', processed_tweet, flags=re.MULTILINE)

                #Removing digits
                processed_tweet = re.sub(r'\d+','', processed_tweet)
                
                # Remove all the special characters
                # processed_tweet = re.sub(r'\W', ' ', processed_tweet)
                    
                # remove all single characters
                processed_tweet = re.sub(r'\s+[a-zA-Z]\s+', ' ', processed_tweet)
            
                # Remove single characters from the start
                processed_tweet = re.sub(r'\^[a-zA-Z]\s+', ' ', processed_tweet) 
            
                # Substituting multiple spaces with single space
                processed_tweet= re.sub(r'\s+', ' ', processed_tweet, flags=re.I)
                # Converting to Lowercase
                processed_tweet = processed_tweet.lower()
                
                processed_tweets += processed_tweet 
            tweetList.append(processed_tweets)
            # print(tweetList)
            # print("========")
            vectorizer = TfidfVectorizer()
            vectors = vectorizer.fit_transform(tweetList)
            feature_names = vectorizer.get_feature_names()
            dense = vectors[0].T.todense()
            df = pd.DataFrame(dense, index=feature_names, columns=["TFIDF"])
            df = df.sort_values('TFIDF', ascending=False)
            df.insert(1, "username", username, True) 
            df.to_csv('hasilFIXBANGET.csv',mode='a')
            # print(vectors[0])

if __name__ == "__main__":

    fileopen  = open("username.txt", 'r') 
    filename = fileopen.readlines()

    # file1=open('DATA_TWEETS.csv','a+',encoding='utf-8')
    # writer = csv.writer(file1)
    # writer.writerow(['username','tweets'])
    # file1.close()

    for i in filename:
        username = i.strip()
        # scrapping(username)
    

    tfidf_count()
    
    fileopen.close()


    # Dinamis 
    # 1. baca txt isi username
    # 2. scrapping per username
    # 3. hasil scrapping >> csv (mau 1 csv apa gabung?)
    # 4. dari csv baru di tfidf per orang!
    # ------------------
