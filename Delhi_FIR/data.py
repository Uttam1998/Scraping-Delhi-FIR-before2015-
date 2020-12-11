import requests
from bs4 import BeautifulSoup
from UVutils import *
from contextlib import closing
import pprint
from datetime import datetime

homepage = r"http://59.180.234.21:85"

def getSoup(request):
    return BeautifulSoup(request.text, 'lxml')

def getInitialData(soup):
    d_viewstate = soup.find(id="__VIEWSTATE")["value"]
    d_viewgen = soup.find(id="__VIEWSTATEGENERATOR")["value"]
    d_eventval = soup.find(id="__EVENTVALIDATION")["value"]

    return d_viewstate, d_viewgen, d_eventval

def getDistrict(soup,
                district,
                session):
    d_viewstate, d_viewgen, d_eventval = getInitialData(soup)
    data = {
        "__EVENTTARGET": "ddlDistrict",
        "__EVENTARGUMENT": "",
        "__LASTFOCUS": "",
        "__VIEWSTATE": d_viewstate,
        "__VIEWSTATEGENERATOR": d_viewgen,
        "__EVENTVALIDATION": d_eventval,
        "ddlYear": "2015",
        "ddlDistrict": district,#district
        "txtRegNo": "",
        "ddlPS": "---SELECT---",
        "txRegFromDt": "",
        "txRegToDt": "",
        "rbtnListAVC": "0"
    }

    res = session.post(homepage, data=data,
                       headers=getheaders())
    if res.status_code == 200:
        soup = getSoup(res)
    else:
        raise Exception("Failed to get data at getDistrict(%s)" % district)

    return soup, session, data

def getPS(soup, ps, session, data):
    d_viewstate, d_viewgen, d_eventval = getInitialData(soup)

    data["__VIEWSTATE"] = d_viewstate
    data["__VIEWSTATEGENERATOR"] = d_viewgen
    data["__EVENTVALIDATION"] = d_eventval
    data["ddlPS"] = ps 

    res = session.post(homepage, data=data,
                       headers=getheaders())

    if res.status_code == 200:
        soup = getSoup(res)
    else:
        raise Exception("Failed to get data at getPS(%s)" % ps)

    return soup, session, data

def getResults(soup, session, district, ps, fir_no):
    d_viewstate, d_viewgen, d_eventval = getInitialData(soup)

    data = {
        "__EVENTTARGET": "",
        "__EVENTARGUMENT": "",
        "__LASTFOCUS": "",
        "__VIEWSTATE": d_viewstate,
        "__VIEWSTATEGENERATOR": d_viewgen,
        "__EVENTVALIDATION": d_eventval,
        "ddlYear": "2015",
        "ddlDistrict": district,#district
        "txtRegNo": fir_no,
        "ddlPS": ps,
        "txRegFromDt": "",
        "txRegToDt": "",
        "rbtnListAVC": "0",
        "btnSearch": "Search"
    }

    res = session.post(homepage, data=data,
                       headers=getheaders())

    if res.status_code == 200:
        soup = getSoup(res)
    else:
        raise Exception("Failed to get data at getResults(%s, %s)" % (district, ps))

    return soup, session

def getviewfir(soup, session, district, ps, fir_no):
    d_viewstate, d_viewgen, d_eventval = getInitialData(soup)

    data = {
        "__EVENTTARGET": "",
        "__EVENTARGUMENT": "",
        "__LASTFOCUS": "",
        "__VIEWSTATE": d_viewstate,
        "__VIEWSTATEGENERATOR": d_viewgen,
        "__EVENTVALIDATION": d_eventval,
        "ddlYear": "2015",
        "ddlDistrict": district,#district
        "txtRegNo": fir_no,
        "ddlPS": ps,
        "txRegFromDt": "",
        "txRegToDt": "",
        "rbtnListAVC": "0",
        "DgRegist$ctl03$imgDelete.x": "3",
        "DgRegist$ctl03$imgDelete.y": "4"
    }

    res = session.post(homepage, data=data,
                       headers=getheaders())

    if res.status_code == 200:
        soup = getSoup(res)
    else:
        raise Exception("Failed to get data at getResults(%s, %s)" % (district, ps))

    return soup, session

def getData(soup, session, data, district, ps, fir_no):
    # soup, session, data = getDistrict(soup, district, session)
    soup, session, data = getPS(soup, ps, session, data)
    soup, session = getResults(soup, session, district, ps, fir_no)
    soup, session = getviewfir(soup, session, district, ps, fir_no)
    res = session.post(homepage, data=data,headers=getheaders())

    table = soup.find("table", { "id" : "GridView1" })
    table_body = table.find_all('tr')
    row1 = table_body[4]
    data = row1.find_all('td')
    #print(len(data))
    #for i in data:
    #      print(i.text)
    data_store = getEmptySchema()
    data_store["district"] = data[2].text.split(':')[-1].strip().lower()
    data_store["police_station"] = data[4].text.split(':')[-1].strip().lower()
    data_store["fir_year"] = data[6].text.split(':')[-1].strip()
    data_store["fir_no"] = data[8].text.split(':')[-1].strip()
    data_store["fir_date"] = getDate(data[10].text)
    data_store["source_url"] = res.url
    #print(data_store)

    #to get act and section
    row2 = table_body[5]
    tr= row2.find_all('tr')
    act_sec_dict = getActsAndSections()
    data=[]
    for i in range(len(tr)):
            td = tr[i].find_all('td')
            data.append(td)
    for i in range(1,len(tr)):
            act_sec_dict["act"].append(data[i][1].text)
            act_sec_dict["section"].append(data[i][2].text.split(':')[-1].strip())
    data_store['act_section'].append(act_sec_dict)
    #print(act_sec_dict)

    # to get petinioner details
    for i in range(20,30):
        t = table_body[i]
        if t.text.split()[0] == "6.":
            sec6 = i + 1
            #print(sec6)
    row3 = table_body[sec6]
    tr = row3.find_all('tr')
    pet_dict = getPetDict()
    data = []
    for i in range(1,len(tr)):
            td = tr[i].find_all('td')
            data.append(td)
    pet_dict["name"] = data[0][1].text.strip().replace(u'\xa0', u' ').lower().partition(" (s/o) ")[0]
    pet_dict["address"] = data[4][1].text.split(':')[-1].strip().lower()
    pet_dict["relative_name"] = data[0][1].text.strip().replace(u'\xa0', u' ').lower().partition(" (s/o) ")[2]
    pet_dict["type"] = 'petitioner'
    data_store['pet_resp'].append(pet_dict)
    #print(pet_dict)

    # to get respondent details
    row4 = table_body[33]
    tr = row4.find_all('tr')
    #print(len(tr))
    #print(tr[0].find_all('td')[1].text)
    res_dict = getresDict()
    data = []
    for i in range(len(tr)):
            td = tr[i].find_all('td')[1] 
            data.append(td)
            res_dict["name"].append(data[i].text.split(':')[-1].strip().lower())
    res_dict['type'] = 'respondent'
    data_store['pet_resp'].append(res_dict)
    #print(res_dict)
    print(data_store)



