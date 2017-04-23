from __future__ import print_function

import requests
import requests.auth
from requests.packages.urllib3.exceptions import InsecureRequestWarning


class InfluxMetrics:
    def __init__(self, url, validate_ssl, user, password):
        self.url = url
        self.validate_ssl = validate_ssl
        self.user = user
        self.password = password

        if not self.validate_ssl:
            requests.packages.urllib3.disable_warnings()

    def report(self, temp, state):
        self.__post("temp value={}".format(temp))

        state_value = 0
        if state:
            state_value = 1
        self.__post("heat value={}".format(state_value))

    def __post(self, data):
        try:
            auth = requests.auth.HTTPBasicAuth(self.user, self.password)
            requests.post(self.url, data=data, auth=auth, verify=self.validate_ssl)
        except Exception as e:
            print(e)
