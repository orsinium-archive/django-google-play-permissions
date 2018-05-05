# built-in
from logging import getLogger

# external
from selenium import webdriver

# app
from .base import WebBase


URL_TEMPLATE = 'https://play.google.com/store/apps/details?id={}&hl=en'
BUTTON = 'View details'


logger = getLogger('djgpp')


class WebInterface(WebBase):
    def connect(self, **credentials):
        """Init PhantomJS driver.
        """
        self.api = webdriver.PhantomJS()

    def download(self, app_id):
        """Get permissions list from app page on google play.

        1. Go to app page.
        2. Click on "View details" button.
        3. Extract permissions list from alert window.
        """
        # open page
        self.api.get(URL_TEMPLATE.format(app_id))
        # click on button
        element = self.api.find_element_by_link_text(BUTTON)
        if not element:
            self.api.save_screenshot('page.png')
            logger.error('WebInterface: button not found.')
            return
        if element.get_property('text') != 'View details':
            self.api.save_screenshot('page.png')
            logger.error('WebInterface: invalid button.')
            return
        element.click()
        # select alert window
        windows = self.api.find_elements_by_xpath('//body/div[4]/div/div[2]/content/*/div')
        if not windows:
            self.api.save_screenshot('page.png')
            logger.error('WebInterface: alert window not found.')
            return
        # iterate by lines
        result = []
        for line in windows[0].find_elements_by_xpath('./div'):
            line = line.get_property('text')
            group, *permissions = line.split('\n')
            group = group.strip()
            permissions = [permission.strip() for permission in permissions if permission]
            result.append((group, permissions))
        return result[1:]
