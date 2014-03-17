Brand cup converter
===================

This script will show how to use the Bratabase API to convert a bra size from one brand to another using cup indexes as translation mechanism.

Usage
=====

To use the script you must have registered a Bratabase application because you will need its credentials to use the API.


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

## Fetch the size range

## Convert the cups
