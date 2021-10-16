from functools import total_ordering


class Sms(object):
    def __init__(self, msg, date):
        self.msg = msg
        self.date = date
        self.month = self.get_month()
    
    def get_month(self):
        split_date =  self.date.split('-')
        return split_date[0] + split_date[1]