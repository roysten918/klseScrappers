import settings as S
from common import connect_url, formStocklist, printable
from utils.dateutils import change2KlseDateFmt, getToday

I3_LATEST_QR_URL = S.I3_KLSE_URL + '/financial/quarter/latest.jsp'
I3_QR_URL = S.I3_KLSE_URL + '/servlets/stk/annqtyres/'


def crawl_latest_qr(trading_date=getToday("%d-%b-%Y")):
    latestQR = scrape_latest_qr(connect_url(I3_LATEST_QR_URL), trading_date)
    return latestQR


def unpack_qr(fy, announce_date, qd, qn,
              rev, pbt, np, np2sh, div, nw, dpp, npmargin, roe,
              nosh, rps, adjRps, eps, adjEps, dps, adjDPS, naps, adjNaps,
              qoq, yoy,
              eoqDate, eoqPrice, eoqPRps, eoqPEps, eoqPNaps, eoqEY, eoqDY,
              anniversaryDate, annPrice, annPRps, annPEps, annPNaps, annEY, annDY):
    if S.DBG_QR:
        print "DBG:{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12}".format(
            qd, qn, rev, pbt, np, div, roe, eps, dps, annEY, annDY, qoq, yoy)
    return [qd, qn, rev, pbt, np, div, roe, eps, dps, annEY, annDY, qoq, yoy]


def scrape_qr(counter, stk_code, soup):
    if soup is None or len(soup) <= 0:
        print ('QR ERR: no result for <' + counter + '>')
        return None
    table = soup.find('table', {'class': 'nc'})
    if table is None:
        if S.DBG_ALL:
            print ('INFO: No QR data is available for <' + counter + "." + stk_code + '>')
        return None
    qr_list = []
    for tr in table.findAll('tr'):
        td = tr.findAll('td')
        # qr = [x.text.strip().replace('&nbsp; ', '').encode("ascii") for x in td]
        qr = [printable(x.text.replace('&nbsp;', '').encode("ascii")).strip() for x in td]
        if S.DBG_QR:
            print("DBG:")
            for x in qr:
                print repr(x)
        if len(qr) > 0:
            qr_list = unpack_qr(*qr)
            break
    return qr_list


def crawl_qr(counter):
    counter = counter.upper()
    slist = formStocklist(counter, S.KLSE_LIST)
    qrUrl = I3_QR_URL + slist[counter] + ".jsp"
    if S.DBG_ALL or S.DBG_QR:
        print ("\tQR: " + counter + " " + slist[counter] + " " + qrUrl)
    qr = scrape_qr(counter, slist[counter], connect_url(qrUrl))
    return qr


def format_qr(counter, qd, qn, rev, pbt, np, div, roe, eps, dps, annEY, annDY, qoq, yoy):
    if S.DBG_ALL or S.DBG_QR:
        print("%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s" %
              (counter, qd, qn, rev, pbt, np, div, roe, eps, dps, annEY, annDY, qoq, yoy))
    tdstr = " > " + counter + ", " + qd + ", Q" + qn + ", rev:" + rev + ", pbt:" \
            + pbt + ", np:" + np + ", div:" + div + ", roe:" + roe + ", eps:" + eps + ", dps:" \
            + dps + ", annEY:" + annEY + ", annDY:" + annDY + ", qoq:" + qoq + ", yoy:" + yoy
    return tdstr


def unpack_latest_qr(num, stock, announcementDate, fy, qd, qn,
                     price, change, pchange,
                     rev, pbt, np, np2sh, div, nw,
                     dpp, npmargin, roe,
                     rps, eps, dps, naps,
                     qoq, yoy):
    if S.DBG_QR:
        print "DBG:{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12}".format(
            stock, announcementDate, qd, qn, rev, pbt, np, div, roe, eps, dps, qoq, yoy)
    return [stock, announcementDate, qd, qn, rev, pbt, np, div, roe, eps, dps, qoq, yoy]


def get_qoq_links(jsp_link):
    soupQR = connect_url(S.I3_KLSE_URL + jsp_link)
    if soupQR is None or len(soupQR) <= 0:
        print ('getQoQLinks ERR: no result')
        return None
    divs = soupQR.find("div", {"id": "container"})
    div = divs.find("div", {"id": "content"})
    tables = div.findAll('table')
    pdf_links = {}
    found = False
    for table in tables:
        for tr in table.findAll('tr'):
            for td in tr.findAll('td'):
                divs = td.findAll('div')
                for div in divs:
                    for tr in div.findAll('tr'):
                        for td in tr.findAll('td'):
                            links = td.findAll('a')
                            for link in links:
                                pdf_link = link.get('href')
                                if pdf_link is None:
                                    continue
                                if "staticfile" in pdf_link:
                                    found = True
                                    fname = link.getText().replace('&nbsp;', '')
                                    pdf_links[S.I3_KLSE_URL + pdf_link] = fname.strip()
                                else:
                                    if found:
                                        break
                            if found:
                                break
                        if found:
                            break
                    if found:
                        break
                if found:
                    break
            if found:
                break
        if found:
            break
    return pdf_links


def scrape_latest_qr(soup, trading_date):
    if soup is None or len(soup) <= 0:
        print ('LatestQR ERR: no result')
        return None
    table = soup.find('table', {'class': 'nc'})
    if table is None:
        if S.DBG_ALL:
            print ('INFO: No Latest QR data is available')
        return None
    qr_list = {}
    for tr in table.findAll('tr'):
        td = tr.findAll('td')
        latestQR = [x.text.strip().replace('&nbsp; ', '').encode("ascii") for x in td]
        # latestQR = [printable(x.text.encode("ascii").replace('&nbsp;', '')).strip() for x in td]
        if S.DBG_QR:
            print("DBG:")
            for x in latestQR:
                print repr(x)
        if len(latestQR) > 0:
            [stock, announcementDate, qd, qn, rev, pbt, np, div, roe, eps, dps, qoq, yoy] = unpack_latest_qr(*latestQR)
            if announcementDate == trading_date:
                if stock not in qr_list:
                    links = tr.findAll('a')
                    jsp_link = ""
                    for link in links:
                        jsp_link = link.get('href')
                        if "QoQ" in jsp_link:
                            jsp_link = get_qoq_links(jsp_link)
                            if len(jsp_link) > 0:
                                break
                    qr_list[stock] = [announcementDate, qd, qn, rev, pbt, np, div, roe, eps, dps, qoq, yoy, jsp_link]
                else:
                    print ("INFO: Duplicated announcement: " + stock + ":" + qd + ":Q" + qn)
            else:
                ann_dt = change2KlseDateFmt(announcementDate, "%d-%b-%Y")
                trd_dt = change2KlseDateFmt(trading_date, "%d-%b-%Y")
                if S.DBG_QR:
                    print("DBG:dates:{0}:{1}".format(ann_dt, trd_dt))
                if ann_dt < trd_dt:
                    break
    return qr_list
