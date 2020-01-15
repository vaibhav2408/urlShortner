"""Custom file to read configs/files"""
import os

import yaml


class ConfigUtils:
    """Class to load configs as per system input_type"""

    @staticmethod
    def read_file(path):
        """
        Reads the yaml/text file and returns the content in yaml/json format
        :param path:
        :return:
        """
        if os.path.join(path).endswith('.yaml'):
            with open(os.path.dirname(os.path.abspath(__name__)) + path) as f:
                configs = yaml.load(f, Loader=yaml.FullLoader)
                return configs
        else:
            with open(os.path.dirname(os.path.abspath(__name__)) + "/" + path, 'r') as f:
                lines = f.readlines()
            lines = [line.strip() for line in lines]
            return lines
