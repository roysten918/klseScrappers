'''
Created on Apr 27, 2018

@author: hwase0ng
'''
from Utils.fileutils import getStockCode
import csv
import settings as S


def loadKlseCounters(infile):
    stocklist = {}
    with open(infile) as f:
        reader = csv.reader(f)
        slist = list(reader)
        if S.DBG_ALL:
            print slist[:3]
        for counter in slist[:]:
            if S.DBG_ALL:
                print "\t", counter[0]
            stocklist[counter[0]] = counter[1]
    return stocklist


def formStocklist(stocks, infile):
    stocklist = {}
    if "," in stocks:
        stocks = stocks.split(",")
    else:
        stocks = [stocks]

    for shortname in stocks:
        stock_code = getStockCode(shortname, infile)
        stocklist[shortname] = stock_code

    return stocklist


def appendCsv(rtn_code, OUTPUT_FILE):
    if rtn_code != 0:
        return

    TMP_FILE = OUTPUT_FILE + 'tmp'

    f = open(OUTPUT_FILE, "ab")
    ftmp = open(TMP_FILE, "r")
    f.write(ftmp.read())
    f.close()
    ftmp.close()


if __name__ == '__main__':
    pass
