"""
This is the (unofficial) Python API for HaveIBeenPwned Website.

Using this code, you can manage to know if your email has been compromised using HaveIBeenPwned's database.

"""
import requests
import json

URL = "https://haveibeenpwned.com/api/v2/breachedaccount/"


class haveibeenpwnedAPI(object):

    """
        haveibeenpwnedAPI Main Handler
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        """
            __new__ builtin
        """
        if not cls._instance:
            cls._instance = super(haveibeenpwnedAPI, cls).__new__(
                cls, *args, **kwargs)
        return cls._instance

    def is_compromised(self, mail):
        resource = URL + mail
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:29.0) Gecko/20100101 Firefox/29.0'}
            r = requests.get(resource, headers=headers, timeout=3, verify=False)
            if r.status_code == 404:
                return []
            else:
                return json.loads(r.content)
        except Exception, e:
            print e.message
            pass
