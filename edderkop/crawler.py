import logging

from bs4 import BeautifulSoup

import requests

from six.moves.urllib.parse import urlparse

import edderkop.models
import edderkop.utils

LOG = logging.getLogger(__name__)


class Crawler(object):
    def __init__(self):
        self.allowed_domains = set()
        self.urls = []
        self.completed_urls = []
        self._session = None
        self.sitemap = edderkop.models.SiteMap()

    def add_urls(self, urls):
        map(self.add_url, urls)

    def add_url(self, url):
        parsed_url = urlparse(url)
        if parsed_url.path == '':
            url += '/'

        if url not in self.urls and url not in self.completed_urls:
            self.urls.append(url)
            self.allowed_domains.add(urlparse(url).hostname)
        else:
            LOG.debug('%s already in the queue or already handled.', url)

    @property
    def session(self):
        if not self._session:
            LOG.debug('Creating session')
            self._session = requests.Session()
        return self._session

    def run(self):
        while self.urls:
            url = self.urls.pop(0)
            LOG.debug('Handling URL: %s', url)
            self.completed_urls.append(url)
            self.inspect_page(url)

        return self.sitemap

    def inspect_page(self, url):
        self.sitemap[url] = edderkop.models.Page(url)
        page = self.fetch_page(url)
        soup = self.parse_page(page)

        for link in self.extract_links(soup, url):
            LOG.debug('%s included a link to %s', url, link)
            self.sitemap[url].links.add(link)

            if urlparse(link).hostname in self.allowed_domains:
                self.add_url(link)

        for img in self.extract_images(soup, url):
            LOG.debug('%s included an image: %s', url, img)
            self.sitemap[url].images.add(img)

        for script in self.extract_scripts(soup, url):
            LOG.debug('%s included a script: %s', url, script)
            self.sitemap[url].scripts.add(script)

    def fetch_page(self, url):
        return self.session.get(url).content

    def parse_page(self, page):
        return BeautifulSoup(page, "lxml")

    def extract_things(self, soup, source_url, tagname, attribute, **filters):
        urlparse(source_url)

        for item in soup.find_all(tagname, **filters):
            if item.has_attr(attribute):
                yield edderkop.utils.target_url(source_url, item[attribute])

    def extract_links(self, soup, source_url):
        return self.extract_things(soup, source_url, 'a', 'href', href=edderkop.utils.href_usable)

    def extract_images(self, soup, source_url):
        return self.extract_things(soup, source_url, 'img', 'src')

    def extract_scripts(self, soup, source_url):
        return self.extract_things(soup, source_url, 'script', 'src')
