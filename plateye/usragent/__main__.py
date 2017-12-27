import sys
from argparse import ArgumentParser

from .crawlers import get_crawler_class_by_name

argument_parser = ArgumentParser('user agent')

argument_parser.add_argument(
    '-crawl',
    metavar='crawler class name',
    help='crawls agents strings by using crawler class and saves them to files'
)

parsed_args = argument_parser.parse_args()

if parsed_args.crawl:
    crawler_object = get_crawler_class_by_name(parsed_args.crawl)()
    if crawler_object is None:
        print("Crawler class was not found!")
        sys.exit()
    crawler_object.crawl()
else:
    argument_parser.print_usage()
