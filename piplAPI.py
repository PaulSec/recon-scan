"""
This is the (unofficial) Python API for Pipl.com Website.
Using this code, you can manage to retrieve info on a specific person with his name.

"""
import requests
from bs4 import BeautifulSoup


class PiplAPI(object):

    """
        PiplAPI Main Handler
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        """
            __new__ builtin
        """
        if not cls._instance:
            cls._instance = super(PiplAPI, cls).__new__(
                cls, *args, **kwargs)
        return cls._instance

    def get_info(self, name):
        url = 'https://pipl.com/search/?q=+%s&l=&sloc=&in=5' % (name)
        # display_message(url)
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
        # for platform_name in res:
        #     print 'On %s:' % (platform_name)
        #     for profile in res[platform_name]:
        #         print '\t%s' % (profile)
        return res
