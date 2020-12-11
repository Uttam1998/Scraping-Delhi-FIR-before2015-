import re
import copy
import pymongo
import hashlib
import boto3
import os

#access_key = os.environ["AWS_ACCESS_KEY_ID"]
#secret_key = os.environ["AWS_SECRET_ACCESS_KEY"]


def getheaders():
    headers = {
    'Origin': 'http://59.180.234.21:85',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.8',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Cache-Control': 'max-age=0',
    'Referer': 'http://59.180.234.21:85/index.aspx',
    'Connection': 'keep-alive',
    }

    return headers


def getEmptySchema():
    data_store = {
        "source": "fir",
        "state": "haryana",
        "district": "",
        "police_station": "",
        "fir_no": "",
        "fir_year": "",
        "fir_date": "",
        "act_section": [],
        "pet_resp": [],
        "source_url": "",
        "s3_url": "",
        "unique_md5": "",
        "added_on": "",
        "status": 1
    }
    return data_store


def getPetDict():
    pet_dict = {
        "name": "",
        "address": "",
        "address_type": "",
        "relative_name": "",
        "relative_type": "",
        "advocate": "",
        "type": ""
    }
    return pet_dict

def getresDict():
    res_dict = {
        "name": [],
        "address": "",
        "address_type": "",
        "relative_name": "",
        "relative_type": "",
        "advocate": "",
        "type": ""
    }
    return res_dict


def getDate(string):
    string = string.split(' ')
    return string[-1].strip()


def getActsAndSections():
        act_sec_dict = {
                "act": [],
                "section":[]
        } 
        return act_sec_dict

