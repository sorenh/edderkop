import unittest

from edderkop import models
from edderkop.formatters import graphviz

expected_output = '''digraph G {
"http://example.com/";
"http://example.com/" -> "http://example2.com/page";
"http://example.com/" -> "http://google.com";
"http://example.com/" -> "http://example.com/images/logo.png";
}
'''


class GraphvizFormatterTests(unittest.TestCase):
    def test_full(self):
        sitemap = models.SiteMap()

        url = 'http://example.com/'
        page = models.Page(url)

        sitemap[url] = page
        page.links = set(['http://example2.com/page', 'http://google.com'])
        page.images = set(['http://example.com/images/logo.png'])
        page.script = set(['http://example2.com/script.js'])

        formatter = graphviz.formatter_class(sitemap, sort_func=sorted)
        self.assertEquals(expected_output, formatter.format())
