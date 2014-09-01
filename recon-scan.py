#!/bin/python
# coding: utf-8

import sys
import requests
from bs4 import BeautifulSoup
import re
import string
# import unicodedata

people = []

# def remove_accents(data):
#     return ''.join((c for c in unicodedata.normalize('NFD', data.decode("utf8")) if unicodedata.category(c) != 'Mn'))


def get_number_of_results(company_name):
    url = 'http://www.yatedo.com/s/companyname:(%s)/normal' % (company_name)
    print url
    req = requests.get(url)
    if 'did not match any' in req.content:
        return 0
    return re.search(r"<span id=\"snb_elm_m\">([\d\s]+)</span>", req.content).group(1).replace(' ', '')


def clean_string(s):
    return filter(lambda x: x in string.printable, s)


def get_people(company_name, start_index, page):
    url = 'http://www.yatedo.com/search/profil?c=normal&q=companyname:(%s)&rlg=en&uid=-1&start=%s&p=%s' % (company_name, start_index, page)
    print url
    req = requests.get(url)
    soup = BeautifulSoup(req.content)
    res = []
    for contact in soup.findAll('div', attrs={'class': 'span4 spanalpha ycardholder'}):
        contact_name = contact.find('a', attrs={})
        contact_job = contact.find('div', attrs={'class': 'ytdmgl'})
        #res.append(contact_name.text)
        contact_name = clean_string(contact_name.text)
        contact_job = clean_string(contact_job.text[:-1])
        print "%s (%s)" % (contact_name, contact_job)
        get_info_on_user(contact_name)
    return res


def get_info_on_user(name):
    url = 'https://pipl.com/search/?q=+%s&l=&sloc=&in=5' % (name)
    print url
    req = requests.get(url)
    soup = BeautifulSoup(req.content)
    #res = {}
    for profile in soup.findAll('div', attrs={'class': 'full_person profiles'}):
        profile_link = profile.find('div', attrs={'class': 'url'}).text.replace(' ', '')
        platform_name = profile.find('div', attrs={'class': 'from'}).text.replace(' ', '').split('-')[1]
        print "\t on %s (%s)" % (platform_name[:-1], profile_link[2:-3])


def main():
    if len(sys.argv) < 2:
        print 'Usage: python yatedo-scan.py <company name>'
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
