#!/bin/python
# coding: utf-8

import sys
import requests
from bs4 import BeautifulSoup
import re

people = []


def get_number_of_results(company_name):
    url = 'http://www.yatedo.com/s/companyname:(%s)/normal' % (company_name)
    print url
    req = requests.get(url)
    if 'did not match any' in req.content:
        return 0
    return re.search(r"<span id=\"snb_elm_m\">([\d\s]+)</span>", req.content).group(1).replace(' ', '')


def get_people(company_name, start_index, page):
    url = 'http://www.yatedo.com/search/profil?c=normal&q=companyname:(%s)&rlg=en&uid=-1&start=%s&p=%s' % (company_name, start_index, page)
    print url
    req = requests.get(url)
    soup = BeautifulSoup(req.content)
    for contact in soup.findAll('div', attrs={'class': 'span4 spanalpha ycardholder'}):
        link_name = contact.find('a', attrs={})
        print link_name.text


def main():
    if len(sys.argv) < 2:
        print '[!] Specify the company name'
        sys.exit(-1)

    print 'Fetching result for company "%s"' % (sys.argv[1])
    res = int(get_number_of_results(sys.argv[1]))

    if res == 0:
        print 'Stopping here, no results for %s' % sys.argv[1]
        sys.exit(-1)

    print 'Found %s results, collecting them..' % (res)
    i = 0
    while i * 16 < res:
        people.append(get_people(sys.argv[1], i * 16, i + 1))
        i = i + 1

if __name__ == '__main__':
    main()
