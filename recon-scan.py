#!/bin/python
# coding: utf-8

import sys
import requests
from bs4 import BeautifulSoup
import re
from optparse import OptionParser
import json

VERBOSE_MODE = False

def display_message(s):
    global VERBOSE_MODE
    if VERBOSE_MODE:
        print '[verbose] %s' % s


def get_number_of_results(company_name):
    url = 'http://www.yatedo.com/s/companyname:(%s)/normal' % (company_name)
    display_message(url)
    req = requests.get(url)
    if 'did not match any' in req.content:
        return 0
    return re.search(r"<span id=\"snb_elm_m\">([\d\s]+)</span>", req.content).group(1).replace(' ', '')


def get_people(company_name, start_index, page):
    url = 'http://www.yatedo.com/search/profil?c=normal&q=companyname:(%s)&rlg=en&uid=-1&start=%s&p=%s' % (company_name, start_index, page)
    display_message(url)
    req = requests.get(url)
    soup = BeautifulSoup(req.content)
    res = []
    for contact in soup.findAll('div', attrs={'class': 'span4 spanalpha ycardholder'}):
        contact_name = contact.find('a', attrs={})
        contact_job = contact.find('div', attrs={'class': 'ytdmgl'})
        contact_name = contact_name.text
        contact_job = contact_job.text[:-1]

        print "%s (%s)" % (contact_name, contact_job)
        # creating structure for the contact
        contact = {}
        contact['name'] = contact_name
        contact['job'] = contact_job
        contact['medias'] = get_info_on_user(contact_name)
        res.append(contact)
    return res


def get_info_on_user(name):
    url = 'https://pipl.com/search/?q=+%s&l=&sloc=&in=5' % (name)
    display_message(url)
    req = requests.get(url)
    soup = BeautifulSoup(req.content)
    res = {}

    # collecting all profiles
    for profile in soup.findAll('div', attrs={'class': 'full_person profiles'}):
        profile_link = profile.find('div', attrs={'class': 'url'}).text.replace(' ', '').replace('\n', '')
        platform_name = profile.find('div', attrs={'class': 'from'}).text.replace(' ', '').replace('\n', '').split('-')[1]
        # print "\t on %s (%s)" % (platform_name, profile_link)
        if platform_name not in res:
            res[platform_name] = []
        res[platform_name].append(profile_link)

    # displaying all profiles we gathered
    for platform_name in res:
        print 'On %s:' % (platform_name)
        for profile in res[platform_name]:
            print '\t%s' % (profile)
    return res


def main():
    global VERBOSE_MODE
    parser = OptionParser()
    parser.add_option("-c", "--company", dest="company", help="Company you want to gather info", default=None)
    parser.add_option("-p", "--person", dest="person", help="Person you want to gather info from", default=None)
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False, help="Verbose mode")

    (options, args) = parser.parse_args()

    if (options.verbose):
        VERBOSE_MODE = True

    if (options.person is None and options.company is None):
        parser.error("Wrong number of arguments")
        sys.exit(-1)

    if (options.company is not None):
        print 'Fetching result for company "%s"' % (options.company)
        num = int(get_number_of_results(options.company))

        if num == 0:
            print 'Stopping here, no results for %s' % options.company
            sys.exit(-1)

        res = {}
        res['company_name'] = options.company
        res['employees'] = []
        print 'Found %s results, collecting them..' % (num)
        i = 0
        while i * 16 < num:
            res['employees'].append(get_people(options.company, i * 16, i + 1))
            i = i + 1
        print json.dumps(res)

    if (options.person is not None):
        print json.dumps(get_info_on_user(options.person))

if __name__ == '__main__':
    main()
