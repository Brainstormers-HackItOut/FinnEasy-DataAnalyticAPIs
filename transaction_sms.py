def get_transaction_info(sms):    
    credit = ['credit','credited']
    debit = ['debit','debited']
    transaction_type = 'none'
    company = 'none'
    amount = 0
    if any([word in sms for word in credit]):
        transaction_type = 'CREDIT'
        amount = extract_amount(sms)
        

    elif any([word in sms for word in debit]):
        transaction_type = 'DEBIT'
        amount = extract_amount(sms)
        company = extract_company(sms)


    return transaction_type,company,amount

def extract_amount(sms):
    import re
    pattern = "(?:Rs\.?|INR)\s*(\d+(?:[.,]\d+)*)|(\d+(?:[.,]\d+)*)\s*(?:Rs\.?|INR)"
    groups = re.search(pattern,sms)
    amount = 0
    if groups:
        amount = groups.group(1)
    return amount

def extract_company(sms):
    import re
    from fuzzywuzzy import process
    from fuzzywuzzy import fuzz
    companies = ['paytm','zomato','swiggy','kotak','icici','hdfc','sbi','reliance','jio','bharatpe']

    pattern = "([a-zA-Z0-9\.\-]{2,256}\@[a-zA-Z][a-zA-Z]{2,64})"
    groups = re.search(pattern,sms)
    company = 'unknown'
    if groups:
        upi = groups.group(1)
        upi = upi.split('@')[0]
        upi_chars = ''

        for char in upi:
            if not char.isnumeric():
                upi_chars += char

        company = process.extract(upi_chars, companies, scorer=fuzz.partial_ratio)[0][0]
         
    return company