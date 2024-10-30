"""Build the nv_statistics novelibre plugin package.
        
Note: VERSION must be updated manually before starting this script.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/nv_statistics
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
import sys

sys.path.insert(0, f'{os.getcwd()}/../../novelibre/tools')
from package_builder import PackageBuilder

VERSION = '0.2.3'


class PluginBuilder(PackageBuilder):

    PRJ_NAME = 'nv_statistics'
    LOCAL_LIB = 'nvstatisticslib'
    GERMAN_TRANSLATION = True

    def __init__(self, version):
        super().__init__(version)
        self.iconDir = '../icons'

    def add_extras(self):
        self.add_icons()


def main():
    pb = PluginBuilder(VERSION)
    pb.run()


if __name__ == '__main__':
    main()
