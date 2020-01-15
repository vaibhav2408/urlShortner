import argparse
import logging as logger
import os
import uuid
from collections import OrderedDict
from logging.handlers import WatchedFileHandler
from urllib.parse import urlparse  # Python 3

import utils.sql_query_builder as builder
import utils.sql_query_executor as executor
from utils.config_utils import ConfigUtils as util
from utils.find_argument_type import FindArgumentType as findType

str_encode = str.encode

configs = util.read_file('/resources/properties.yaml')

os.makedirs(configs['log_file_directory'], exist_ok=True)
LOG_FILENAME = configs['log_file_directory'] + 'logs.txt'

"""
Setting the date format for log message
"""
date_str = "%m/%d/%Y %I:%M:%S %p"
"""
Adding Handler Filter for Adding Host Name
"""
stream_handler = logger.StreamHandler()
file_handler = WatchedFileHandler(LOG_FILENAME)

"""
Setting up the format of the log message.
"""
fmt_str = '%(asctime)s: [%(threadName)-2.12s] %(levelname)s: [%(filename)s: "%(funcName)s: Line:%(lineno)d] - %(message)s'
file_handler.setFormatter(logger.Formatter(fmt_str))
stream_handler.setFormatter(logger.Formatter(fmt_str))
"""
Initializing a logger and setting up the format
"""

logger.basicConfig(
    handlers=[
        stream_handler,
        file_handler],
    level=logger.INFO,
    datefmt=date_str)

logger.info('Setting up logger.')
logger.info('logs path - {}'.format(LOG_FILENAME))

holder = OrderedDict()

"""Setting the host name"""
host = configs['hostname']


class UrlShorten:
    database = configs['database']

    """ Defines the max number of characters in a short url at a given time."""
    present_size_of_url_string = configs['present_size_of_url_string']

    """Defines the upper limit of characters in the shortened URL at any time."""
    max_allowed_number_characters_in_short_url = configs['max_allowed_number_characters_in_short_url']

    builder = builder.SQLQueryBuilder(configs['table_name'])

    def __init__(self):
        """Creates a table (if not exists)"""
        executor.create_table(self.database, self.builder.build_create_table_query())

    def print_all(self):
        """
        Prints all the entries in the table WEB_URL
        """
        res = executor.execute_command(self.database, self.builder.build_select_all_query())
        for entry in res.fetchall():
            logger.info(entry, '\n')

    @staticmethod
    def my_random_string(string_length=10):
        """Returns a random string of length string_length."""
        random = str(uuid.uuid4())  # Convert UUID format to a Python string.
        random = random.replace("-", "")  # Remove the UUID '-'.
        return random[0:string_length]  # Return the random string.

    def shorten(self, user_input):
        """
        Identifies the type of the input
        Whether it's a file or a url and calls the method to shorten the url
        @:param: the input that user provided
        """
        input_type = findType.find_argument_type(user_input)

        if input_type == 'file':
            logger.info('Given input is a file')
            content = util.read_file(user_input)
            index = 1
            for url in content:
                if index % 10000 == 0:
                    logger.info('finished : {value}'.format(value=index))
                short_url = self.shorten_url(url)
                logger.info('Short url : {url}'.format(url=short_url))
                original_url = self.redirect(short_url)
                logger.info('Re-directing to : {url}'.format(url=original_url))
                index += 1

        else:
            logger.info('Given input is a URL')
            short_url = self.shorten_url(user_input)
            logger.info('Short url : {url}'.format(url=short_url))
            original_url = self.redirect(short_url)
            logger.info('Re-directing to : {url}'.format(url=original_url))

            # urlShorten.print_all()

    def shorten_url(self, original_url):
        url = str_encode(original_url)
        if urlparse(url).scheme == '':
            url = 'http://' + original_url

        shortened_url = host + self.my_random_string(self.present_size_of_url_string)

        is_short_url_unique = self.lookup(shortened_url)

        while not is_short_url_unique:
            self.present_size_of_url_string += 1
            shortened_url = host + self.my_random_string(self.present_size_of_url_string)
            if self.present_size_of_url_string > self.max_allowed_number_characters_in_short_url:
                self.present_size_of_url_string = 1
            if self.lookup(shortened_url):
                break

        executor.execute_command_with_params(self.database, self.builder.build_insert_query(), [shortened_url, url])
        return shortened_url

    def lookup(self, shortened_url):
        """Check whether the generated shortened URL is unique or no
        @:param : shortened_url - the newly generated shortened url
        @:return : true if the URL is unique, else false
        """
        res = executor.execute_command_with_params(self.database, self.builder.build_select_query(), [shortened_url])
        result = res.fetchall()

        if not result:
            return True
        return False

    def get_original_url(self, shortened_url):
        """ Queries the table for a given short URL and returns the original URL"""
        res = executor.execute_command_with_params(self.database, self.builder.build_select_query(), [shortened_url])
        try:
            short = res.fetchone()
            if short is not None:
                url = short[0]
        except Exception as e:
            logger.error(e)
        return url.decode("utf-8")

    def redirect(self, short_url):
        return self.get_original_url(short_url)


if __name__ == "__main__":
    urlShorten = UrlShorten()

    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    args = parser.parse_args()
    user_input = args.input
    urlShorten.shorten(user_input)
