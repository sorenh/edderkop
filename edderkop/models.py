class SiteMap(dict):
    pass


class Page(object):
    def __init__(self, url):
        self.url = url
        self.links = set()
        self.images = set()
        self.scripts = set()
