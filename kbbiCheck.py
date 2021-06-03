from kbbi import KBBI,TidakDitemukan
import pandas as pd
import re
import tweepy
import csv
import string
import math
import time

def checkKbbi(word):
    # try:
    #     KBBI(word)
    # except TidakDitemukan as e:
    #     return word
    with open('indonesian-words.txt') as f:
        if word in f.read():
            return None
        else:
            return word

def remove_unwanted_cols(dataset,cols):
    for col in cols:
        del dataset[col]
    return dataset

def tweetProcessing():
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
    usernameAndWords = {} #dict untuk menyimpan username, dan kata2nya (tweets) dari setiap orang
    totalData = [] #list dari semua username dan tweets 
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
                
                #Removing hexadecimal
                processedTweet = re.sub(r'\\x..','', str(rawData[tweet]))
                
                # Removing hashtag + username
                processedTweet = re.sub(r'\@\w+|\#','',  processedTweet)

                # Removing urls
                processedTweet = re.sub(r"http\S+|www\S+|https\S+", '', processedTweet, flags=re.MULTILINE)

                #Removing digits
                # processedTweet = re.sub(r'\d+','', processedTweet)
                
                #Removing \n
                processedTweet = re.sub(r'\\n',' ', processedTweet)
                
                # Remove all the special characters
                processedTweet = re.sub(r'[^\\\w]', ' ', processedTweet)
                    
                # remove all single characters
                processedTweet = re.sub(r'\s+[a-zA-Z]\s+', ' ', processedTweet)
            
                # Remove single characters from the start
                processedTweet = re.sub(r'\^[a-zA-Z]\s+', ' ', processedTweet) 
            
                # Substituting multiple spaces with single space
                processedTweet= re.sub(r'\s+', ' ', processedTweet, flags=re.I)

                # Converting to Lowercase
                processedTweet = processedTweet.lower()
                
                #Untuk menggabungkan seluruh tweet ke dalam satu list 
                tweetList.extend(processedTweet.split(' '))

            slangWords = [] #list dari kata2 yang tidak ditemukan di kbbi
            for i in range(len(tweetList)): #looping sesuai panjang kalimat
                resultWords = checkKbbi(tweetList[i]) #kalau tidak ditemukan di kbbi, dimasukin ke list
                if resultWords is None:
                    pass
                else:
                    slangWords.append(resultWords)
                # time.sleep(3)

            #dictionary untuk menyimpan data dari username dan slang words nya
            usernameAndWords = {
                "username" : username,
                "words" : slangWords
            }
            totalData.append(usernameAndWords) #list dari semua username yang isinya uname dan slang wordsnya

    return totalData

if __name__ == "__main__":
    hasil = tweetProcessing()

    df = pd.DataFrame(hasil,columns=["username","words"])
    #df.insert(1, "username", tfidfUsername[i], True)
    #df = df.sort_values('TFIDF', ascending=False)
    df.to_csv('slangWords.csv',mode='a')

