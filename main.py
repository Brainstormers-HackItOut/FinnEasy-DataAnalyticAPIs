from re import search
from typing import List

from numpy.core import records
from Sms import Sms
from twitter_sentiment import retrieving_tweets_polarity
from transaction_sms import get_transaction_info
from company_details_from_symbol import get_company_details
from fastapi import FastAPI , UploadFile , File
from aadhar_card_verification import *
from fastapi.responses import JSONResponse

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
async def getTransactionInfo(sms_list: List[Sms]):

    response = {'CREDIT' : {} , 'DEBIT' : {}}
    for sms in sms_list:
        transaction_type,company,amount = get_transaction_info(sms.msg)

        split_date =  sms.date.split('-')
        month =  split_date[0] + '-' +split_date[1]

        if transaction_type == 'DEBIT' and amount != 'none':
            if month not in response['DEBIT']:
                response['DEBIT'][month] = {}

            if company in response['DEBIT'][month]:
                response['DEBIT'][month][company] += float(amount)
            else:
                response['DEBIT'][month][company] = float(amount)

        elif transaction_type == 'CREDIT' and amount != 'none':
            if month not in response['CREDIT']:
                response['CREDIT'][month] = 0

            response['CREDIT'][month] += float(amount)
            

    return response

@app.get("/search")
async def searchBSE(query:str):
    search_result = get_company_details(query)
    return JSONResponse(content = search_result.to_dict(orient = "records"))

@app.post(
    "/aadhar-verification",
    )
async def _aadhar_verification(aadhar_number: str, aadhar_card: UploadFile = File(...)):
      aadhar_number_extracted = aadhar_card_info(aadhar_card)
      if aadhar_number_extracted == "Not found!":
            return JSONResponse(
                content = {
                    "status": False,
                    "message": aadhar_number_extracted
                }
            )     
      verification = pattern_match(aadhar_number_extracted,aadhar_number)
      return JSONResponse(
            content = {
                "status": verification,
                "message": "Extracted aadhar number: " + aadhar_number_extracted
            }
        )
