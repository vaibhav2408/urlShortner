import argparse

from url_shortner import UrlShorten

shortner = UrlShorten()
parser = argparse.ArgumentParser()
parser.add_argument("input")
args = parser.parse_args()
user_input = args.input

"""Calling the method to shorten the url"""
shortner.shorten(user_input)
