"""
Can be used to determine if the given input is an URL or a file
"""
from pathlib import Path


class FindArgumentType:

    @staticmethod
    def find_argument_type(input_arg):
        """
        Returns whether input is a file-path or url
        :param input_arg: the input
        :return: 'file' if it's a file else 'url'
        """
        if input_arg.endswith('.txt'):
            return 'file'
        else:
            file_path = Path(input_arg)
            if file_path.exists():
                return 'file'

            return 'url'
