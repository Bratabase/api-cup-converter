#!/usr/bin/env python

import sys
import json
import argparse
from urllib import urlencode
from urllib2 import urlopen, Request


API_ROOT = 'https://api.bratabase.com/'


def print_brands(brands):
    print 'Available brands:'
    print '\n'.join(['[%s]\t%s' % (pos, b['name'])
        for pos, b in enumerate(brands, 1)])


def print_range(size_range):
    print 'Available sizes'
    for band_line in size_range:
        print ', '.join([s['size'] for s in band_line['sizes']])


class Converter(object):

    def __init__(self, app, key, host, dest_slug):
        self.app_id = app
        self.api_key = key
        self.host = host
        self.dest_brand = dest_slug
        self.dest_brand_conver_url = self.get_dest_brand(dest_slug)

    def get_url(self, url):
        req = Request(url, None, {
            'app_key': self.app_id,
            'secret': self.api_key
        })
        resp = urlopen(req)
        payload = json.loads(resp.read())
        return payload

    def get_root(self):
        return self.get_url(self.host)

    def get_dest_brand(self, brand_slug):
        root = self.get_root()
        # Obtain the brands' collection URL
        brands_url = root['links']['brands']
        # Query the brands' collection by slug with the ?slug= GET
        # parameter
        dest_brand = '%s?%s' % (brands_url, urlencode({
            'slug': brand_slug
        }))
        result = self.get_url(dest_brand)

        # There will only be one brand that matches the required slug
        # If no brand matched the slug the result will be an empty
        # collection. That will cause this to break, but for simplicity
        # sake we won't be doing validation.
        dest_brand_url = result['collection'][0]['href']

        # Fetch the detail of the brand with the desired slyg
        brand_detail = self.get_url(dest_brand_url)

        # And we fetch its sizing URL, that we will be using to query
        # the index size to get the desired destination bra size.
        size_convert_url = brand_detail['links']['main_sizing']
        return size_convert_url

    def ask_brand(self):
        root = self.get_root()
        brands_url = root['links']['brands']
        # Fetching the brands collection. We are only retrieving the first
        # page.
        brands = self.get_url(brands_url)['collection']
        print_brands(brands)
        brand_pos = int(raw_input('Select brand (enter number): '), 10)
        return brands[brand_pos - 1]

    def ask_size(self, brand):
        brand_url = brand['href']
        brand_detail = self.get_url(brand_url)
        sizing_url = brand_detail['links']['main_sizing']
        main_sizing = self.get_url(sizing_url)['body']
        print_range(main_sizing['range'])
        size = raw_input('Type a size: ')

        # Here we could just validate from the already printed
        # main_sizing['range'], but for example's sake, we'll query the
        # endpoint again demonstrating that you can query by GET parameter
        # ?size= to filter the range.
        size_query = '%s?%s' % (sizing_url, urlencode({
            'size': size
        }))
        main_sizing = self.get_url(size_query)['body']

        # We are assuming that the selected size is within the printed
        # range, otherwise it means the size does not exist for the brand
        # and this line will break as the [0] keys will not exist because
        # they will be empty arrays.
        index_size = main_sizing['range'][0]['sizes'][0]['index']
        return index_size

    def convert_size(self, index_size):
        query_url = '%s?%s' % (self.dest_brand_conver_url, urlencode({
            'index_size': index_size
        }))
        main_sizing = self.get_url(query_url)['body']

        # Check the the `range` attribute has any entries, each entry
        # should be a band, so if there are no sizes, then there would be
        # no bands in the result
        if len(main_sizing['range']) == 0:
            sys.exit('%s does not make size %s' % (self.dest_brand,
                index_size))

        # Check that the range's first band only match) has any sizes
        # This means that the size requested is in a band that the brand
        # makes, but if the `sizes` array is empty it means that the cup
        # isn't
        if len(main_sizing['range'][0]['sizes']) == 0:
            sys.exit('%s does not make size %s' % (self.dest_brand,
                index_size))

        size = main_sizing['range'][0]['sizes'][0]['size']
        return size

    def start_interactive(self):
        """
        Ask the user to pick a brand, a size and then return the
        equivalent size in the other brand.
        """
        brand = self.ask_brand()
        size_index = self.ask_size(brand)
        dest_size = self.convert_size(size_index)
        print 'Size for %s is %s' % (self.dest_brand, dest_size)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Indicate API key')
    parser.add_argument('--key')
    parser.add_argument('--app')
    parser.add_argument('--host', default=API_ROOT)
    parser.add_argument('--brand', default='comexim')
    args = parser.parse_args()
    converter = Converter(args.app, args.key, args.host, args.brand)
    converter.start_interactive()
