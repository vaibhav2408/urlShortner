from url_shortner import UrlShorten
from utils.config_utils import ConfigUtils as my_util

if __name__ == "__main__":
    urlShorten = UrlShorten()

    test_file_path = 'test_links.txt'

    print('\n\nRunning test for file as input - \n')

    print('Given input is a file')
    content = my_util.read_file(test_file_path)
    index = 1
    for url in content:
        short_url = urlShorten.shorten_url(url)
        print('Short url : ', short_url)
        original_url = urlShorten.redirect(short_url)
        print('Re-directing to : ', original_url)
        index += 1

    print('\n\nRunning test for URL as input - \n')

    test_url = 'https://docs.python.org/3/howto/argparse.html'
    print('Given input is a URL')
    short_url = urlShorten.shorten_url(test_url)
    print('Short url : ', short_url)
    original_url = urlShorten.redirect(short_url)
    print('Re-directing to : ', original_url)
