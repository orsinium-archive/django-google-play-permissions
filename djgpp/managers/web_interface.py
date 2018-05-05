from selenium import webdriver
from .base import Base
from ..models import Permission


URL_TEMPLATE = 'https://play.google.com/store/apps/details?id={}&hl=en'
BUTTON = 'View details'


class WebInterface(Base):
    def connect(self, **credentials):
        self.api = webdriver.PhantomJS()

    def download(self, app_id):
        # open page
        self.api.get(URL_TEMPLATE.format(app_id))
        # click on button
        element = self.api.find_element_by_link_text(BUTTON)
        if not element:
            return
        if element.get_property('text') != 'View details':
            return
        element.click()
        # select alert window
        windows = self.api.find_elements_by_xpath('//body/div[4]/div/div[2]/content/*/div')
        if not windows:
            return
        # iterate by lines
        result = []
        for line in windows[0].find_elements_by_xpath('./div'):
            line = line.get_property('text')
            group, *permissions = line.split('\n')
            group = group.strip()
            permissions = [permission.strip() for permission in permissions if permission]
            result.append((group, permissions))
        return result

    def parse(self, data):
        objects = []
        for group, permissions in data:
            for name in permissions:
                objects.append(self.get_object(name, group))
        return objects

    def get_object(self, name, group_name):
        parent, _created = Permission.objects.get_or_create(
            text=self.format_name(group_name),
            parent=None,
        )
        obj, _created = Permission.objects.get_or_create(
            text=self.format_name(name),
            defaults=dict(parent=parent),
        )
        return obj

    def format_name(self, name):
        return name[0].upper() + name[1:]
