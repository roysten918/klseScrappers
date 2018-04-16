'''
Created on Dec 26, 2016

@author: t.roy
'''

#  Configurations
WORK_DIR = '.'
SHORTLISTED_FILE = ''
I3PRICEURL = 'https://klse.i3investor.com/servlets/stk/rec/'
HEADERS = {
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
}

# Features toggle
DBG_ALL = True
DBG_ICOM = True
RESUME_FILE = True  # False = fresh reload from ABS_START date, True = only download from next date of last record
PRICE_WITHOUT_SPLIT = True  # False - Apply adjusted close by default
