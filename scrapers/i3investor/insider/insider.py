"""
Usage: main [options] [COUNTER] ...

Arguments:
    COUNTER                     Optional counters
Options:
    -d,--date=<trading_date>    Use provided trading date to search
    -s,--skip=<name>            skip email to name
    -t,--test=<test_name>       run test on selected function

Created on Mar 7, 2020

@author: hwaseong
"""
from common import loadCfg
from scrapers.i3investor.insider.add_listing import crawl_listing
from scrapers.i3investor.insider.entitlements import crawl_entitlement
from scrapers.i3investor.insider.format_insiders import *
from scrapers.i3investor.insider.latest import crawl_latest
from scrapers.i3investor.insider.financial_ar import *
from scrapers.i3investor.insider.financial_qr import *
from scrapers.i3investor.insider.insider_old import crawl_insider
from scrapers.i3investor.insider.price_target import crawl_price_target
from utils.dateutils import getToday
from docopt import docopt
import settings as S
import styles as T
import yagmail
import yaml


def process(stock_list="", trading_date=getToday('%d-%b-%Y')):
    print("Trading date: " + trading_date)
    latest_dir, latest_shd, latest_com = crawl_latest(trading_date)
    latest_div, latest_bonus = crawl_entitlement(trading_date)
    latest_listing = crawl_listing(trading_date)
    latest_target = crawl_price_target(trading_date)
    latest_ar = crawl_latest_ar(trading_date)
    latest_qr = crawl_latest_qr(trading_date)
    if len(stock_list):
        if "," in stock_list:
            stocks = stock_list.split(",")
        else:
            stocks = [stock_list]
        dir_list, shd_list, qr_list, ar_list = [], [], [], []
        for stock in stocks:
            stock = stock.upper()
            di, shd = crawl_insider(stock, trading_date)
            if di is not None and len(di) > 0:
                for item in di:
                    dir_list.append(item)
            if shd is not None and len(shd) > 0:
                for item in shd:
                    shd_list.append(item)
            if stock in latest_qr:
                qr = latest_qr[stock]
                qr_list.append(format_latest_qr(stock, *qr))
            if stock in latest_ar:
                ar = latest_ar[stock]
                ar_list.append(format_latest_ar(stock, *ar))
            if len(dir_list) > 0:
                print ("{header}{lst}".format(header="\tdirectors:", lst=dir_list))
            if len(shd_list) > 0:
                print ("{header}{lst}".format(header="\tshareholders", lst=shd_list))
            # qr = crawlQR(counter)
            # if len(qr) > 0:
            #     print ("{header}{lst}".format(header="QR", lst=formatQR(counter, *qr)))
            if stock in latest_qr:
                qr = latest_qr[stock]
                print (format_latest_qr(stock, *qr))
            if stock in latest_ar:
                ar = latest_ar[stock]
                print (format_latest_ar(stock, *ar))
    else:
        stream = open("scrapers/i3investor/insider/insider.yaml", 'r')
        docs = yaml.load_all(stream, Loader=yaml.FullLoader)
        for doc in docs:
            for name, items in doc.items():
                # print (name + " : " + str(items))
                addr = items["email"]
                print (name + ": " + ", ".join(addr))
                if name == skip_name:
                    print ("\tSkipped")
                    break
                for tracking_list in items.iterkeys():
                    if tracking_list == "email":
                        continue
                    print ("\t" + tracking_list)
                    dir_list, shd_list, com_list, qr_list, ar_list = [], [], [], [], []
                    div_list, bns_list, listing_list, target_list = [], [], [], []
                    dir_title = "Latest Directors Transactions"
                    shd_title = "Latest Substantial Shareholders Transactions"
                    com_title = "Latest Company Transactions"
                    qr_title = "Quarterly Results"
                    ar_title = "Annual Reports"
                    div_title = "Latest Dividend"
                    bns_title = "Latest Bonus, Share Split & Consolidation"
                    listing_title = "Latest Listing"
                    target_title = "Price Target"
                    for stock in items[tracking_list]:
                        stock = stock.upper()
                        '''
                        # res = match_selection(stock, latest_dir, dir_title)
                        # if len(res) > 0:
                        #     for item in res:
                        #         dir_list.append(item)
                        # shd = match_selection(stock, latest_shd, shd_title)
                        # if len(shd) > 0:
                        #     for item in shd:
                        #         shd_list.append(item)
                        # com = match_selection(stock, latest_com, com_title)
                        # if len(com) > 0:
                        #     for item in com:
                        #         com_list.append(item)
                        if stock in latest_dir:
                            dr = latest_dir[stock]
                            for item in dr:
                                dir_list.append(format_director(True, *item))
                        if stock in latest_shd:
                            shd = latest_shd[stock]
                            for item in shd:
                                shd_list.append(format_shareholder(True, *item))
                        if stock in latest_com:
                            com = latest_com[stock]
                            for item in com:
                                com_list.append(format_company(True, *item))
                        '''
                        f = format_decorator(format_director)
                        f(stock, latest_dir, dir_list)
                        f = format_decorator(format_shareholder)
                        f(stock, latest_shd, shd_list)
                        f = format_decorator(format_company)
                        f(stock, latest_com, com_list)
                        if stock in latest_qr:
                            qr = latest_qr[stock]
                            qr_list.append(format_latest_qr(stock, *qr))
                        if latest_ar is not None and stock in latest_ar:
                            ar = latest_ar[stock]
                            ar_list.append(format_latest_ar(stock, *ar))
                        if stock in latest_div:
                            div = latest_div[stock]
                            div_list.append(format_div(stock, *div))
                        if stock in latest_bonus:
                            bns = latest_bonus[stock]
                            bns_list.append(format_dividend(stock, *bns))
                        if stock in latest_listing:
                            listing = latest_listing[stock]
                            listing_list.append(format_listing(stock, *listing))
                        if stock in latest_target:
                            target = latest_target[stock]
                            target_list.append(format_target(stock, *target))
                    format_table_insiders(dir_title, dir_list)
                    format_table_insiders(shd_title, shd_list)
                    format_table_insiders(com_title, com_list)
                    format_ar_qr_table(qr_title, qr_list)
                    format_ar_qr_table(ar_title, ar_list)
                    format_table_entitlement(div_title, div_list)
                    format_table_entitlement(bns_title, bns_list)
                    format_table_listing(listing_title, listing_list)
                    format_table_target(target_title, target_list)
                    list_result = \
                        div_list + bns_list + qr_list + ar_list + dir_list + \
                        shd_list + com_list + listing_list + target_list
                    if len(list_result) > 0:
                        list_result.insert(0, T.t01)
                        subject = "INSIDER UPDATE on {} for portfolio: {}".format(
                            getToday("%d-%b-%Y"), tracking_list.upper()
                        )
                        yagmail.SMTP(S.MAIL_SENDER, S.MAIL_PASSWORD).send(addr, subject, list_result)


# python decorator as high order function
def format_decorator(func):
    def wrapper(stock, latest_list, new_list):
        if stock in latest_list:
            dr = latest_list[stock]
            for item in dr:
                new_list.append(func(True, *item))

    return wrapper


def match_selection(counter, latest_list, list_title):
    if len(latest_list) == 0:
        return ""
    director = "Directors" in list_title
    company = "Company" in list_title
    insiders = []
    for list_item in latest_list:
        if counter == list_item[0]:
            if company:
                [stock, announce_date, from_date, to_date,
                 chg_type, shares, min_price, max_price, total, view] = list_item
                insiders.append(format_company(True, stock, announce_date,from_date, to_date,
                                               chg_type, shares, min_price, max_price, total, view))
            else:
                if director:
                    [stock, announce_date, name, chg_date, chg_type, shares, price, view] = list_item
                else:
                    price = ""
                    [stock, announce_date, name, chg_date, chg_type, shares, view] = list_item
                insiders.append(format_insider(True, director, stock, announce_date, name, chg_date,
                                               chg_type, shares, price, view))
    return insiders


if __name__ == '__main__':
    args = docopt(__doc__)
    cfg = loadCfg(S.DATA_DIR)

    global skip_name
    skip_name = args['--skip']
    insider_date = args['--date']
    counters = ""
    if args['COUNTER']:
        counters = args['COUNTER'][0].upper()
    if args['--test']:
        html_output = True
        if args['--test'] == "listing":
            result = crawl_listing(insider_date, html_output)
        if args['--test'] == "target":
            result = crawl_price_target(insider_date, html_output)
        if html_output:
            result.insert(0, T.t01)
            yagmail.SMTP(S.MAIL_SENDER, S.MAIL_PASSWORD). \
                send("roysten.tan@gmail.com", "INSIDER UPDATE: " + getToday("%d-%b-%Y"), result)
        else:
            for i in result:
                print i
    else:
        if insider_date is not None:
            process(counters, insider_date)
        else:
            process(counters)

    print ('\n...end processing')
