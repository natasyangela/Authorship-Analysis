import pandas as pd
import re
import tweepy
import csv
import string
import math

def scraping(username):
    access_token = '528154427-gBB0wjsslCqhSKmpAAOdVabhz8NgrFIrm28eHYKG'
    access_token_secret = 'bEUzJC2b2O40IcBI2K7VA8xDiqvor9bIuoUcuxFnjv4rz'
    api_key = 'ql4wvYMDOEzAayjRthZBazXm7'
    api_secret_key = 'I7dodoD4rouTJOwwP9r6MrsgEHF2YvJ7CsMeYwJwTdNlmjsp2G'

    auth = tweepy.OAuthHandler(api_key, api_secret_key)
    auth.set_access_token(access_token, access_token_secret)
    
    api = tweepy.API(auth,wait_on_rate_limit=True)
        
    user_timeline = api.user_timeline(username, count=2000, include_rts=False)

    fileTweets = open('2ndData01.csv','a+',encoding='utf-8')
    writer = csv.writer(fileTweets)
    for tweet in user_timeline:
        idStat = tweet.id_str
        status = api.get_status(idStat,tweet_mode = "extended")
        full_text = status.full_text
        writer.writerow([username,str(full_text.encode('utf-8'))[2:-1]])

    fileTweets.close()

def remove_unwanted_cols(dataset,cols):
    for col in cols:
        del dataset[col]
    return dataset

def numOfWordsCount(bagOfWords):
    
    numOfWords = dict.fromkeys(bagOfWords,0)
    for word in bagOfWords:
        numOfWords[word] += 1
    
    return numOfWords

def TFCount(bagOfWords):
    numOfWords = numOfWordsCount(bagOfWords)
    tfDict = {}
    bagOfWordsCount = len(bagOfWords)
    for word, count in numOfWords.items():
        tfDict[word] = count / float(bagOfWordsCount)

    return tfDict

def IDFCount(numOfWordsList):
    idfDict = {}
    # print(numOfWordsList)
    N = len(numOfWordsList)
    # print(N)
    
    for i in range(N):
        idfDict.update(dict.fromkeys(numOfWordsList[i].keys(), 0))
    
    # print(idfDict)

    for document in numOfWordsList:
        for word, val in document.items():
            if val > 0:
                idfDict[word] += 1
    
    for word, val in idfDict.items():
        idfDict[word] = math.log(N / float(val))
    
    return idfDict

def TFIDFCount(tfTotal, idf, tfidfUsername):
    # tfidf = {}
    # looping dalam list TF
    for i in range (len(tfTotal)):
        tfidf = dict.fromkeys(idf.keys(), 0)
        for word, val in tfTotal[i].items():
            tfidf[word] = val * idf[word]

        df = pd.DataFrame.from_dict(tfidf, orient='index',columns=["TFIDF"])
        df.insert(1, "username", tfidfUsername[i], True)
        df = df.sort_values('TFIDF', ascending=False)
        df.to_csv('hasilTFIDF.csv',mode='a')

    # return df

def ProcessData():
    data = pd.read_csv('2ndDATA01.csv',encoding='iso-8859-9')    

    usernameList = data['username']
    tweets = remove_unwanted_cols(data,['username'])
    start = 0
    end =-1
    #start adalah index awal, end adalah pembatas kalo beda username

    N=0 # N adalah total dokumen untuk hitung IDF 
    combineTweets = [] #gabungan tweets dari semua username yang ada
    numOfWordsList = [] #list yang isinya dict numofwords dari masing2 username
    tfTotal = [] #list yang isinya adalah seluruh tf yang ada
    tfidfUsername = [] #list untuk menyimpan username yang jumlahnya sesuai dengan banyak org yg di scraping
    for i in range(len(usernameList.index)):  
        if (i == len(usernameList.index)-1 or usernameList[i] != usernameList[i+1] ):
            username = usernameList[i]
            tfidfUsername.append(username)
            tweetList = []
            start = end +1
            end = i
            rawData = tweets.iloc[start:end+1,0].values #untuk membaca data dari index dan kolom
            # N adalah total dokumen untuk hitung IDF 
            N += 1

            for tweet in range(0, len(rawData)):  
                processedTweet = str(rawData[tweet])

                # Removing hashtag + username
                processedTweet = re.sub(r'\@\w+|\#','', str(rawData[tweet]))

                # Removing urls
                processedTweet = re.sub(r"http\S+|www\S+|https\S+", '', processedTweet, flags=re.MULTILINE)

                #Removing digits
                # processedTweet = re.sub(r'\d+','', processedTweet)
                
                # Removing hexa
                processedTweet = re.sub(r'\\x..','', processedTweet)

                #Removing \n
                processedTweet = re.sub(r'\\n',' ', processedTweet)

                # Taking only special characters
                processedTweet = re.sub(r'\w',' ', processedTweet)

                # Remove all the special characters
                # processedTweet = re.sub(r'[^\\\w]', ' ', processedTweet)
                    
                # remove all single characters
                # processedTweet = re.sub(r'\s+[a-zA-Z]\s+', ' ', processedTweet)
            
                # Remove single characters from the start
                # processedTweet = re.sub(r'\^[a-zA-Z]\s+', ' ', processedTweet) 
            
                # Substituting multiple spaces with single space
                # processedTweet= re.sub(r'\s+', ' ', processedTweet, flags=re.I)

                # Converting to Lowercase
                processedTweet = processedTweet.lower()
                
                #Untuk menggabungkan seluruh tweet ke dalam satu list 
                
                tweetList.extend(processedTweet.split(' '))
                tweetList = list(filter(None, tweetList))

            # ====================== BAGIAN TF ===================
            # panggil def baru untuk itung manual
            # tf = TFCount(tweetList)
            # print(tf)
            # tfTotal.append(tf)
            # print(tweetList)


            # untuk gabungin tweet semua username
            # combineTweets.extend(tweetList)

            # hasil hitung karakter 
            CharCountResult = numOfWordsCount(tweetList)
            # print(hasil)

            df = pd.DataFrame.from_dict(CharCountResult, orient='index',columns=["Jumlah Karakter"])
            df = df.sort_values('Jumlah Karakter', ascending=False)
            df.insert(1, "username", username, True)
            df.to_csv('count character.csv',mode='a')

            #buat list yang isinya numOfWords masing2 username
            # numOfWordsList.append(numOfWordsCount(tweetList))

    # print(numOfWordsList)
    # print(tfTotal)
    # ====================== BAGIAN IDF ===================
    # panggil function IDFCount
    # print(N)
    # idf = IDFCount(numOfWordsList)
    # print(idf)

    # df = pd.DataFrame.from_dict(idf, orient='index',columns=["IDF"])
    # df = df.sort_values('IDF', ascending=False)
    # df.to_csv('hasilIDF_3.csv',mode='a')

    # =======================BAGIAN TFIDF ====================
    # panggil function TFIDFCount
    # tfidf = TFIDFCount(tfTotal,idf,tfidfUsername)

if __name__ == "__main__":

    # fileopen  = open("username10.txt", 'r') 
    # filename = fileopen.readlines()

    #untuk tulis di paling atas, username dan tweets
    #file1=open('2ndDATA01.csv','a+',encoding='utf-8')
    #writer = csv.writer(file1)
    #writer.writerow(['username','tweets'])
    #file1.close()

    #looping baca dari txt, untuk scrapping
    # for i in filename:
    #     username = i.strip()
    #     scraping(username)

    #panggil function untuk hitung TFIDF
    ProcessData()
    
    # fileopen.close()

    # Flow code ^___^
    # 1. baca txt isi username
    # 2. scrapping per username
    # 3. hasil scrapping dalam satu csv namanya DATA_TWEETS
    # 4. Panggil function TFIDFCount
    # 5. Di dalam function itu, baca dari csv, per username
    # 6. Bersihin datanya
    # 7. Panggil function TFCount
    # 8. Panggil function IDFCount
    # ------------------
