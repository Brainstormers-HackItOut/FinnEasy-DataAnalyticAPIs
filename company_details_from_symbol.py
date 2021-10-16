from enum import Flag
from re import search


def get_company_details(query):

    import pandas as pd
    from fuzzywuzzy import fuzz


    thresh = 65
    top_n = 10
    company_data = pd.read_csv("EQUITY_L.csv")

    def getSimilarity(row):        
        return fuzz.partial_ratio(query,row["NAME OF COMPANY"])

    company_data["score"] = company_data.apply(getSimilarity,axis=1)
    company_data = company_data.sort_values("score",ascending=False)
    top_n_results = company_data[:top_n]

    return top_n_results

    