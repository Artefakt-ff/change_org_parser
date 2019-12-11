from langdetect import detect
from requests import get
import re


def no_panic(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            print(e)

    return wrapper


class Petition:
    BASE_URL = 'https://www.change.org'
    petition_fields = ['title', 'description', 'subscribers_num', 'subscribers_num_goal', 'place', 'date']

    def __init__(self, petition_dict):
        self.title = petition_dict.get('title', '')
        self.description = petition_dict.get('description', '')
        self.subscribers_num = petition_dict.get('subscribers_num', '')
        self.subscribers_num_goal = petition_dict.get('subscribers_num_goal', '')
        self.link = petition_dict.get('link', '')
        self.place = detect(self.title)
        self.date = ''

    @staticmethod
    def common_formatter(text):
        if text is not None:
            return text.replace('\n', '').replace('  ', ' ').replace(',', '')
        return text

    @no_panic
    def format(self):
        self.title = self.common_formatter(self.title)
        if self.description != '':
            self.description = self.common_formatter(self.description[:self.description.index('… Далее')])
        self.subscribers_num = self.common_formatter(self.subscribers_num.split(' ')[0])
        try:
            self.subscribers_num_goal = self.common_formatter(self.subscribers_num_goal.split(' ')[2])
        except IndexError:
            pass
        self.link = self.BASE_URL + self.link
        self.date = self.get_date(self.link)

    def serialize(self):
        self.format()
        data = [self.__getattribute__(field) for field in self.petition_fields]
        return ','.join(data) + '\n'

    @no_panic
    def get_date(self, link):
        resp = get(link, headers={'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                                  'cookie': '%7B%22locale%22%3A%22ru-RU%22%2C%22countryCode%22%3A%22AM%22%7D;'})
        if resp.status_code != 200:
            print(f'wrong link: {link}')
            return
        content = str(resp.content)
        regex = re.compile(r"\"createdAt\":\"(.+?)\"")
        if 'createdAt' in content:
            date = regex.search(content).group(1)
            return date
        return ''

    def get_fields(self):
        return ','.join(self.petition_fields)
