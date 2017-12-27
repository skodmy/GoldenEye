#!/usr/bin/env python

import sys
from abc import ABC, abstractmethod
from urllib.request import urlopen

from bs4 import BeautifulSoup


class UserAgentExampleStringsCrawler(ABC):
    host = ''
    url = ''

    @abstractmethod
    def parse(self, web_resource):
        raise NotImplementedError

    def crawl(self):
        try:
            with urlopen(self.url) as web_resource:
                beautiful_soup = BeautifulSoup(web_resource.read(), "html.parser")
        except ValueError as error:
            print(error)
        else:
            return self.parse(beautiful_soup)


class WhatIsMyBrowserCrawler(UserAgentExampleStringsCrawler):
    host = 'https://developers.whatismybrowser.com'
    url = 'https://developers.whatismybrowser.com/useragents/explore/'

    # def __init__(self):
    #     self.url.format('useragents/explore/')

    def parse(self, web_resource):
        web_resource = web_resource.find('ul', {'id': 'listing-by-field-name'})
        for li in web_resource.find_all('li'):
            if li.ul is not None:
                for lli in li.ul:
                    a = lli.find('a')
                    if a != -1:
                        with urlopen(self.host + a['href']) as header:
                            with open('res/{}'.format(a.text.lower()), 'w') as out_file:
                                soup = BeautifulSoup(header.read(), "html.parser")
                                print()
                                # for td in soup.find_all('td', {'class': 'useragent'}):
                                    # print(td)
                                    # out_file.write(td.a.text.strip(' \t\n\r'))


# def fetch_user_agents_lists(url: str):
#     try:
#         with urllib.request.urlopen(url) as web_file:
#             soup = BeautifulSoup(web_file.read(), "html.parser")
#     except ValueError as error:
#         print(error)
#     else:
#         user_agents = soup.find('div', {'id': 'liste'}).find_all('li')
#         print(user_agents)
#         if len(user_agents) <= 0:
#             print("No UAs Found. Are you on http://www.useragentstring.com/ lists?")
#             sys.exit(0)
#         for user_agent in user_agents:
#             print(user_agent.get_text().strip(' \t\n\r'))
