def get_transaction_info(sms):    
    credit = ['credit','credited']
    debit = ['debit','debited']
    transaction_type = 'none'
    amount = 0
    if any([word in sms for word in credit]):
        transaction_type = 'CREDIT'
        amount = extract_amount(sms)

    elif any([word in sms for word in debit]):
        transaction_type = 'DEBIT'
        amount = extract_amount(sms)

    return transaction_type,amount

def extract_amount(sms):
    import re
    pattern = "(?:Rs\.?|INR)\s*(\d+(?:[.,]\d+)*)|(\d+(?:[.,]\d+)*)\s*(?:Rs\.?|INR)"
    groups = re.search(pattern,sms)
    amount = 0
    if groups:
        amount = groups.group(1)
    return amount