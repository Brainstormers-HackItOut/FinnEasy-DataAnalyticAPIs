def retrieving_tweets_polarity(symbol):

    import constants as ct
    import pandas as pd
    import tweepy
    import preprocessor as p
    import re
    from textblob import TextBlob
    from Tweet import Tweet

    stock_ticker_map = pd.read_csv('Yahoo-Finance-Ticker-Symbols.csv')
    stock_full_form = stock_ticker_map[stock_ticker_map['Ticker']==symbol]
    symbol = stock_full_form['Name'].to_list()[0][0:12]

    auth = tweepy.OAuthHandler(ct.consumer_key, ct.consumer_secret)
    auth.set_access_token(ct.access_token, ct.access_token_secret)
    user = tweepy.API(auth)
        
    tweets = tweepy.Cursor(user.search_tweets, q=symbol, tweet_mode='extended', lang='en',exclude_replies=True).items(ct.num_of_tweets)
        
    tweet_list = [] #List of tweets alongside polarity
    global_polarity = 0 #Polarity of all tweets === Sum of polarities of individual tweets
    tw_list=[] #List of tweets only => to be displayed on web page
    #Count Positive, Negative to plot pie chart
    pos=0 #Num of pos tweets
    neg=1 #Num of negative tweets
    for tweet in tweets:
        count=20 #Num of tweets to be displayed on web page
        #Convert to Textblob format for assigning polarity
        tw2 = tweet.full_text
        tw = tweet.full_text
            #Clean
        tw=p.clean(tw)
        #print("-------------------------------CLEANED TWEET-----------------------------")
        #print(tw)
        #Replace &amp; by &
        tw=re.sub('&amp;','&',tw)
        #Remove :
        tw=re.sub(':','',tw)
        #print("-------------------------------TWEET AFTER REGEX MATCHING-----------------------------")
        #print(tw)
        #Remove Emojis and Hindi Characters
        tw=tw.encode('ascii', 'ignore').decode('ascii')

        #print("-------------------------------TWEET AFTER REMOVING NON ASCII CHARS-----------------------------")
        #print(tw)
        blob = TextBlob(tw)
        polarity = 0 #Polarity of single individual tweet
        for sentence in blob.sentences:
                
            polarity += sentence.sentiment.polarity
            if polarity>0:
                pos=pos+1
            if polarity<0:
                neg=neg+1
            
            global_polarity += sentence.sentiment.polarity
        if count > 0:
            tw_list.append(tw2)
            
        tweet_list.append(Tweet(tw, polarity))
        count=count-1
    if len(tweet_list) != 0:
        global_polarity = global_polarity / len(tweet_list)
    else:
        global_polarity = global_polarity
    neutral=ct.num_of_tweets-pos-neg

    if neutral<0:
        neg=neg+neutral
        neutral=20

    if global_polarity>0:
        tw_pol="Overall Positive"
    else:
        tw_pol="Overall Negative"

    return global_polarity,tw_list,tw_pol,pos,neg,neutral