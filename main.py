'''
Created on Apr 16, 2018

@author: hwase0ng
'''

import settings as S
import pandas as pd
from scrapers.i3investor.scrapeRecentPrices import connectRecentPrices, scrapeEOD, unpackEOD
from scrapers.i3investor.scrapeStocksListing import writeStocksListing,\
    writeLatestPrice
from Utils.dateutils import getLastDate, getDayBefore, getToday
from scrapers.investingcom.scrapeInvestingCom import loadIdMap, InvestingQuote,\
    scrapeKlseRelated
from common import formStocklist, loadKlseCounters, appendCsv
from Utils.fileutils import cd, purgeOldFiles
import os
import json
import sys


def scrapeI3eod(sname, scode, lastdt):
    eodStock = scrapeEOD(connectRecentPrices(scode), lastdt)
    if eodStock is None or not eodStock:
        print "ERR:No Result for ", sname, scode
        return None
    i3eod = []
    for key in sorted(eodStock.iterkeys()):
        if key <= lastdt:
            print "Skip downloaded: ", key, lastdt
            continue
        i3eod += [sname + ',' + key + ',' +
                  ','.join(map(str, unpackEOD(*(eodStock[key]))))]
    return i3eod


def getStartDate(OUTPUT_FILE):
    if S.RESUME_FILE:
        startdt = getLastDate(OUTPUT_FILE)
        if len(startdt) == 0:
            # File is likely to be empty, hence scrape from beginning
            startdt = S.ABS_START
    else:
        startdt = S.ABS_START
    return startdt


def scrapeI3(stocklist):
    for shortname in sorted(stocklist.iterkeys()):
        if shortname in S.EXCLUDE_LIST:
            print "INF:Skip: ", shortname
            continue
        stock_code = stocklist[shortname]
        if len(stock_code) > 0:
            rtn_code = -1
            OUTPUT_FILE = S.DATA_DIR + shortname + "." + stock_code + ".csv"
            TMP_FILE = OUTPUT_FILE + 'tmp'
            startdt = getStartDate(OUTPUT_FILE)
            print 'Scraping {0},{1}: lastdt={2}'.format(
                shortname, stock_code, startdt)
            i3eod = scrapeI3eod(shortname, stock_code, startdt)
            if i3eod is None or not i3eod:
                continue
            rtn_code = 0
            f = open(TMP_FILE, "wb")
            for eod in i3eod:
                f.write(eod + '\n')
                if S.DBG_ALL:
                    print eod
            f.close()
        else:
            print "ERR: Not found: ", shortname
            rtn_code = -1

        appendCsv(rtn_code, OUTPUT_FILE)


def checkLastTradingDay(lastdt):
    idmap = loadIdMap('scrapers/investingcom/klse.idmap')
    eod = InvestingQuote(idmap, 'ZHULIAN', getDayBefore(lastdt))
    if isinstance(eod.response, unicode):
        dfEod = eod.to_df()
        if isinstance(dfEod, pd.DataFrame):
            dates = pd.to_datetime(dfEod["Date"], format='%Y%m%d')
            dates = dates.dt.strftime('%Y-%m-%d').tolist()
            if S.DBG_ALL:
                print dates
            return dates
    return None


def backupKLse(prefix):
    if len(BKUP_DIR) == 0 or not BKUP_DIR.endswith('\\'):
        print "Skipped backing up data", BKUP_DIR
        return

    with cd(BKUP_DIR):
        os.system('pwd')
        bkfl = prefix + 'klse' + getToday() + '.tgz'
        cmd = 'tar czvf ' + bkfl + ' -C ' + S.DATA_DIR + ' *.csv'
        print cmd
        # os.system(cmd)
        os.system('backup.sh ' + bkfl + ' ' + S.DATA_DIR)


def preUpdateProcessing():
    if len(BKUP_DIR) == 0:
        print 'Nothing to do.'
        return

    try:
        print "Pre-update Processing ...", BKUP_DIR
        with cd(BKUP_DIR):
            purgeOldFiles('*.tgz', 10)
        '''
        with cd(S.DATA_DIR):
            backupKLse("pre")
        '''
        print "Pre-update Processing ... Done"
    except Exception, e:
        print e
        pass


def postUpdateProcessing():
    backupKLse("pst")

    if len(MT4_DIR) == 0:
        return

    with cd(BKUP_DIR):
        os.system('mt4.sh ' + MT4_DIR)
        print "Post-update Processing ... Done"


def loadSetting(c):
    global BKUP_DIR
    global MT4_DIR
    BKUP_DIR = c["main"]["BKUP_DIR"]
    MT4_DIR = c["main"]["MT4_DIR"]
    # Allows DATA_DIR to be overwritten here
    try:
        datadir = c["main"]["DATA_DIR"]
        if len(datadir) > 0 and datadir.endswith('/'):
            S.DATA_DIR = datadir
    except Exception:
        pass


def loadCfg():
    try:
        # Refers backup drive instead of DATA_DIR which is in network share
        with open(S.DATA_DIR + 'config.json') as json_data_file:
            cfg = json.load(json_data_file)
            loadSetting(cfg)
            return cfg
    except EnvironmentError:
        print "Missing config.json file"
        sys.exit(1)


def scrapeKlse():
    '''
    stocks = 'AASIA,ADVPKG,AEM,AIM,AMTEK,ASIABRN,ATLAN,ATURMJU,AVI,AYER,BCB,BHIC,BIG,BIPORT,BJFOOD,BJMEDIA,BLDPLNT,BOXPAK,BREM,BRIGHT,BTM,CAMRES,CEPCO,CFM,CHUAN,CICB,CNASIA,CYMAO,DEGEM,DIGISTA,DKLS,DOLMITE,EIG,EKSONS,EPMB,EUROSP,FACBIND,FCW,FSBM,GCE,GETS,GOCEAN,GOPENG,GPA,HCK,HHHCORP,HLT,ICAP,INNITY,IPMUDA,ITRONIC,JASKITA,JETSON,JIANKUN,KAMDAR,KANGER,KIALIM,KLCC,KLUANG,KOMARK,KOTRA,KPSCB,KYM,LBICAP,LEBTECH,LIONDIV,LIONFIB,LNGRES,MALPAC,MBG,MELATI,MENTIGA,MERGE,METROD,MGRC,MHCARE,MILUX,MISC,MSNIAGA,NICE,NPC,NSOP,OCB,OFI,OIB,OVERSEA,PENSONI,PESONA,PGLOBE,PJBUMI,PLB,PLS,PTGTIN,RAPID,REX,RSAWIT,SANBUMI,SAPIND,SBAGAN,SCIB,SEALINK,SEB,SERSOL,SHCHAN,SINOTOP,SJC,SMISCOR,SNC,SNTORIA,SRIDGE,STERPRO,STONE,SUNSURIA,SUNZEN,SYCAL,TAFI,TFP,TGL,THRIVEN,TSRCAP,UMS,UMSNGB,WEIDA,WOODLAN,XIANLNG,YFG,ZECON,ZELAN'
    '''
    stocks = ''

    S.DBG_ALL = False
    S.RESUME_FILE = True

    klse = "scrapers/i3investor/klse.txt"
    if len(stocks) > 0:
        #  download only selected counters
        scrapeI3(formStocklist(stocks, klse))
    else:
        '''
        Determine if can use latest price found in i3 stocks page
        Conditions:
          1. latest eod record in csv file is not today
          2. latest eod record in csv file is 1 trading day behind
             that of investing.com latest eod
        '''
        lastdt = getLastDate(S.DATA_DIR + 'ZHULIAN.5131.csv')
        dates = checkLastTradingDay(lastdt)
        if dates is None or (len(dates) == 1 and dates[0] == lastdt):
            print "Already latest. Nothing to update."
            postUpdateProcessing()
        else:
            if len(dates) == 2 and dates[1] > lastdt and dates[0] == lastdt:
                useI3latest = True
            else:
                useI3latest = False

            if useI3latest:
                preUpdateProcessing()
                writeLatestPrice(True, dates[1])
            else:
                # Full download using klse.txt
                # To do: a fix schedule to refresh klse.txt
                writeStocksListing = False
                if writeStocksListing:
                    print "Scraping i3 stocks listing ..."
                    writeStocksListing(klse)

                # TODO:
                # I3 only keeps 1 month of EOD, while investing.com cannot do more than 5 months
                # May need to do additional checking to determine if need to use either
                scrapeI3(loadKlseCounters(klse))

            scrapeKlseRelated('scrapers/investingcom/klse.idmap', S.DATA_DIR)

    print "\nDone."


if __name__ == '__main__':
    cfg = loadCfg()
    '''
    preUpdateProcessing()
    '''
    scrapeKlse()
    pass
