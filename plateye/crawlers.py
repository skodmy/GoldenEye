#!/usr/bin/env python

import sys
from abc import ABC, abstractmethod
from urllib.request import urlopen

from bs4 import BeautifulSoup


class UserAgentExampleStringsCrawler(ABC):
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
    url = 'https://developers.whatismybrowser.com/useragents/explore/'

    # def __init__(self):
    #     self.url.format('useragents/explore/')

    def parse(self, web_resource):
        web_resource = web_resource.find('ul', {'id': 'listing-by-field-name'})
        for li in web_resource:
            gen = (ul for ul in li.find('ul') if ul != -1)
            for ili in gen:
                print(ili.find('a'))
        # print(web_resource)


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
