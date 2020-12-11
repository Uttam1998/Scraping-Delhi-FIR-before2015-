import requests
from bs4 import BeautifulSoup
from data import getSoup, getData, getDistrict
from UVutils import getheaders
from contextlib import closing
import re


if __name__ == '__main__':
    homepage = r"http://59.180.234.21:85"
    session = requests.Session()
    headers = getheaders()
    res = session.get(homepage, headers=headers, verify=False)
    soup = BeautifulSoup(res.text,"lxml")

    pattern_district = re.compile(r"<option value=\"([0-9]+)\">(.+)</option>")
    with (closing(open('district_names.txt', 'r', encoding='utf8'))) as file:
        districts = " ".join(file.readlines())
    district_pairs = pattern_district.findall(districts)
    #print(district_pairs)

    for district_pair in district_pairs:
        print("Scraping for District -> ", district_pair[1])
        soup, session, data = getDistrict(soup, district_pair[0],
                                                   session)
        ps_values = soup.find("select", id="ddlPS").select("option")
        ps_dict = {}
        for ps in ps_values[1:]:
            ps_dict[ps.text] = ps["value"]
        #print(ps_dict)
        for ps_name, value in ps_dict.items():
            print("Scraping content for PS {}".format(ps_name))
            for i in range(1000):
                fir_no =str('{:d}'.format(i).zfill(4))
                try:
                    getData(soup, session, data, district_pair[0], value, fir_no)
                except:
                    pass