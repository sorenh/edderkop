import argparse
import importlib
import logging
import sys


from edderkop.crawler import Crawler
from edderkop.receivers.collector import Collector


def get_formatter_class(formatter='graphviz'):
    mod = importlib.import_module('edderkop.formatters.%s' % (formatter,))
    return mod.formatter_class


def main(argv=sys.argv[1:]):
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)-15s %(message)s')

    parser = argparse.ArgumentParser(description='web crawler')
    parser.add_argument('--formatter', help='Which formatter to use [json,graphviz] [default:graphviz]', default='graphviz')
    parser.add_argument('urls', metavar='URL', nargs='+', help='Starting point for the crawling process')
    options = parser.parse_args(argv)

    receiver = Collector()

    crawler = Crawler(receiver)
    crawler.add_urls(options.urls)

    for x in crawler.run():
        pass

    formatter = get_formatter_class(options.formatter)(receiver.sitemap)
    print(formatter.format())

    return True


if __name__ == '__main__':
    sys.exit(not main(sys.argv[1:]))  # pragma: nocover
