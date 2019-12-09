from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep

from app.parser.Petition import Petition


class Parser:
    BASE_URL = 'https://www.change.org/petitions'

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.closed = False
        self.raw_petitions = []
        self.formatted_petitions = []

    def __del__(self):
        if not self.closed:
            self.driver.close()

    def get_petitions_page(self, scrolls: int):
        self.driver.get(self.BASE_URL)
        btn = self.driver.find_element_by_xpath(
            "//*[contains(text(), 'Показать больше')]")
        for i in range(scrolls):
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            btn.click()
            sleep(2)

        page = self.driver.page_source
        self.driver.close()
        self.closed = True
        return page

    def parse_petitions(self, page):
        bs = BeautifulSoup(page, features='html.parser')
        petitions = bs.find_all(
            "a", class_='link-block')
        self.raw_petitions = petitions
        return petitions

    def format_petitions(self):
        for petition in self.raw_petitions:
            format_petition = dict()
            format_petition['link'] = petition['href']
            format_petition['title'] = petition.find('h4', class_='mtn').text
            try:
                format_petition['description'] = petition.find('p',
                                                               class_='mtxxs').text
            except AttributeError:
                pass
            format_petition['subscribers_num'] = petition.find('strong').text
            format_petition['subscribers_num_goal'] = \
                petition.find('p', class_='type-s ptxxs') \
                    .find('span', class_='type-weak').text
            self.formatted_petitions.append(format_petition)
        return self.formatted_petitions

    def get_petitions(self, amount):
        page = self.get_petitions_page(amount // 5)
        self.parse_petitions(page)
        self.format_petitions()
        petitions = []
        for i, petition_dict in enumerate(self.formatted_petitions):
            try:
                petition = Petition(petition_dict)
                if i == 0:
                    petitions.append(petition.get_fields())
                petitions.append(petition)
            except Exception:
                continue
        return petitions
