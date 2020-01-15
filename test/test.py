import unittest

from url_shortner import UrlShorten
from utils.config_utils import ConfigUtils as my_util


class TestStringMethods(unittest.TestCase):
    def test_url_shortening_with_file_as_input(self):
        url_shorten = UrlShorten()

        test_file_path = 'test_links.txt'

        content = my_util.read_file(test_file_path)

        for url in content:
            short_url = url_shorten.shorten_url(url)
            original_url = url_shorten.redirect(short_url)
            self.assertTrue(url, original_url)

    def test_url_shortening_with_url_as_input(self):
        url_shorten = UrlShorten()

        test_url = 'https://docs.python.org/3/howto/argparse.html'
        short_url = url_shorten.shorten_url(test_url)
        original_url = url_shorten.redirect(short_url)
        self.assertTrue(test_url, original_url)


if __name__ == '__main__':
    unittest.main()
