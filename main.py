from twitter_sentiment import retrieving_tweets_polarity
from fastapi import FastAPI

app = FastAPI()

@app.get("/sentiment/{symbol}")
async def getPolarity(symbol):
    global_polarity,tw_list,tw_pol,pos,neg,neutral = retrieving_tweets_polarity(symbol)

    return {'global_polarity' : global_polarity,
    'tw_list' : tw_list,
    'tw_pol' : tw_pol,
    'pos' : pos,
    'neg' : neg,
    'neutral' : neutral}
