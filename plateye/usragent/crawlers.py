"""

"""
import os
import sys
from abc import ABC, abstractmethod
from urllib.request import urlopen, urljoin
from re import search

from bs4 import BeautifulSoup
from tqdm import tqdm

from ..settings import USER_AGENT_STRINGS_FILES_DIRS_ROOT_DIR


class UserAgentExampleStringsCrawler(ABC):
    host = ''
    crawl_url = ''
    save_dir = ''

    def __init__(self):
        self.save_dir = os.path.join(
            USER_AGENT_STRINGS_FILES_DIRS_ROOT_DIR, self.__class__.__name__.replace('Crawler', '').lower()
        )
        if not os.path.exists(self.save_dir):
            os.mkdir(self.save_dir)

    @abstractmethod
    def parse(self, beautiful_soup):
        raise NotImplementedError

    def crawl(self):
        try:
            with urlopen(self.crawl_url) as web_resource:
                beautiful_soup = BeautifulSoup(web_resource.read(), "html.parser")
        except ValueError as error:
            print(error)
        else:
            return self.parse(beautiful_soup)


class WhatIsMyBrowserCrawler(UserAgentExampleStringsCrawler):
    host = 'https://developers.whatismybrowser.com'
    crawl_url = 'https://developers.whatismybrowser.com/useragents/explore/'

    def parse(self, beautiful_soup):
        for field_name_li in beautiful_soup.find('ul', {'id': 'listing-by-field-name'}).find_all('li'):
            if field_name_li.ul is not None:
                for field_values_ul_li in field_name_li.ul:
                    fld_nm_pg_a = field_values_ul_li.find('a')
                    if fld_nm_pg_a != -1:
                        number_of_pages = int(search(r'\d+', str(field_values_ul_li)).group())
                        print("Number of pages for {} = {}".format(fld_nm_pg_a.text, number_of_pages))
                        print("Select pages range to download from: ")
                        try:
                            start = int(input("start from page: "))
                            stop = int(input("stop on page: "))
                            if start <= 0 or stop <= 0 or start > stop:
                                raise ValueError
                        except (ValueError, TypeError, KeyboardInterrupt) as error:
                            if isinstance(error, KeyboardInterrupt):
                                sys.exit(0)
                            start = 1
                            stop = number_of_pages
                            print(
                                "Invalid values were provided!",
                                "Not a correct range of integers!",
                                "[{}, {}] will be used instead!".format(start, stop)
                            )
                        with open(os.path.join(self.save_dir, fld_nm_pg_a.text.lower() + '.txt'), 'w') as out_file:
                            for page_number in tqdm(range(start, stop + 1), desc="Parsing %s pages" % fld_nm_pg_a.text):
                                with urlopen(urljoin(self.host, fld_nm_pg_a['href'], str(page_number))) as header:
                                    soup = BeautifulSoup(header.read(), "html.parser")
                                    for td in soup.find_all('td', {'class': 'useragent'}):
                                        out_file.write(td.a.text.strip(' \t\n\r') + '\n')


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
