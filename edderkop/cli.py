import argparse
import importlib
import logging
import sys


from edderkop.crawler import Crawler


def get_formatter_class(formatter='graphviz'):
    mod = importlib.import_module('edderkop.formatters.%s' % (formatter,))
    return mod.formatter_class


def main(argv=sys.argv[1:]):
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)-15s %(message)s')

    parser = argparse.ArgumentParser(description='web crawler')
    parser.add_argument('--formatter', help='Which formatter to use [json,graphviz] [default:graphviz]', default='graphviz')
    parser.add_argument('urls', metavar='URL', nargs='+', help='Starting point for the crawling process')
    options = parser.parse_args(argv)

    crawler = Crawler()
    crawler.add_urls(options.urls)
    sitemap = crawler.run()

    formatter = get_formatter_class(options.formatter)(sitemap)
    print(formatter.format())

    return True


if __name__ == '__main__':
    sys.exit(not main(sys.argv[1:]))  # pragma: nocover
