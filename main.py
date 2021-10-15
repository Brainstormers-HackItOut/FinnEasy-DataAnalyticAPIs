from typing import List
from twitter_sentiment import retrieving_tweets_polarity
from transaction_sms import get_transaction_info
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

@app.post("/transaction-info")
async def getTransactionInfo(sms_list: List[str]):

    response = {}
    for sms in sms_list:
        transaction_type,amount = get_transaction_info(sms)
        response[sms] = {"type": transaction_type,"amount":amount}

    return response
    
