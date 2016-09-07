import edderkop.models


class Collector(object):
    def __init__(self):
        self.sitemap = edderkop.models.SiteMap()

    def add_page(self, url):
        self.sitemap[url] = edderkop.models.Page(url)

    def add_link(self, source, target):
        self.sitemap[source].links.add(target)

    def add_image(self, source, img):
        self.sitemap[source].images.add(img)

    def add_script(self, source, script):
        self.sitemap[source].scripts.add(script)
