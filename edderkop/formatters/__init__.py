class Formatter(object):
    def __init__(self, sitemap, sort_func=None):
        self.sitemap = sitemap

        if sort_func:
            self.sort_func = sort_func
        else:
            self.sort_func = lambda l: l

    def format(self):
        out = self.header()
        out += self.body()
        out += self.footer()
        return out

    def sort(self, l):
        return self.sort_func(l)

    def body(self):
        out = ''
        for page in self.sort(self.sitemap):
            out += self.format_page(page)

            for link in self.sort(self.sitemap[page].links):
                out += self.format_link(page, link)

            for image in self.sort(self.sitemap[page].images):
                out += self.format_image(page, image)

            for script in self.sort(self.sitemap[page].scripts):
                out += self.format_script(page, script)

        return out
