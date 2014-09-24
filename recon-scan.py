#!/bin/python
# coding: utf-8

import sys
from optparse import OptionParser
# external APIs
from yatedoAPI import YatedoAPI
from piplAPI import PiplAPI
from emailFormatAPI import EmailFormatAPI
from haveibeenpwnedAPI import haveibeenpwnedAPI


VERBOSE_MODE = False


def display_message(s):
    global VERBOSE_MODE
    if VERBOSE_MODE:
        print '[verbose] %s' % s


def main():
    global VERBOSE_MODE
    parser = OptionParser()
    parser.add_option("-c", "--company", dest="company", help="Company you want to gather info", default=None)
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False, help="Verbose mode")

    (options, args) = parser.parse_args()

    if options.verbose:
        VERBOSE_MODE = True

    if options.company is None:
        parser.print_help()
        sys.exit(-1)

    # get employees
    display_message('Retrieving employees for the company "%s"' % (options.company))
    company = YatedoAPI().get_employees(options.company)
    display_message('%s employees found' % (len(company['employees'])))

    # retrieve info for each employee
    for employee in company['employees']:
        display_message('Retrieving info for user "%s"' % (employee['name']))
        employee['infos'] = PiplAPI().get_info(employee['name'])
         # displaying all profiles we gathered
        for platform_name in employee['infos']:
            print 'On %s:' % (platform_name)
            for profile in employee['infos'][platform_name]:
                print '\t%s' % (profile)

    # retrieve emails
    mails = EmailFormatAPI().get(options.company)
    display_message('%s mails found' % (len(mails)))
    for mail in mails:
        display_message('"%s" pwned? %s' % (mail, haveibeenpwnedAPI().is_compromised(mail) != []))

if __name__ == '__main__':
    main()
