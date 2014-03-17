Brand cup converter
===================

This script will show how to use the Bratabase API to convert a bra size from one brand to another using cup indexes as translation mechanism.

Usage
=====

To use the script you must have [registered a Bratabase application](http://developers.bratabase.com/register-app/) because you will need its credentials to use the API.


    $ ./cup_convert.py --app=YOUR_APP_ID --key=APP_SECRET --brand=BRAND_SLUG

Where:

* **YOUR_APP_ID**: Is the application ID.
* **APP_SECRET**: The application's secret key.
* **BRAND_SLUG**: The __slug__ of the brand you want to convert cups to. You can obtain this from http://bratabsae.com and check the URL of any brand.


You will be shown the top 20 brands and pick one of them.
Then the API will print the size range it manufactures and ask you to enter one of them.
Finally it will print the cup in the destination brand.

How it works
============

## Fetch the brands

In order to show the list of brands to pick from, the script will GET to the API root url `https://api.bratabase.com` and then follow the `links.brands` key to fetch the [brand's collection](http://developers.bratabase.com/brands-endpoint/).

It will parse the `collection` key of the payload and display the list of brands received. This will be the top 20 bands (first page of the collection).

## Fetch the size range

When the user makes a selection, we use the previously fetched list of brands and obtain the `href` key of it that contains the link to that [brand's detail endpoint](http://developers.bratabase.com/brand-detail/).

After GETting that resource, we go to its `links.main_sizing` key to get the URL of this brand's main [sizing scheme detail](http://developers.bratabase.com/brand-sizing-detail/).

We use the `body.range` key to get the table of available sizes for the brand and render that to ask the user to make a selection.

## Convert the cups

Once we have a size from the user, we query the sizing detail page [filtering by `size`](http://developers.bratabase.com/brand-sizing-detail/#By-size), from that result we obtain the corresponding `index` size of the selection.
We then go to the destination brand's sizing endpoint and this time we [query by `index_size`](http://developers.bratabase.com/brand-sizing-detail/#By-index_size) this time to obtain the size that matches this brand's index size. The only result should tell us in the `size` attribute the destination size we're looking for.

If the result of the 2nd query is an empty `range` that means that the requested index size does not exist for the brand.
