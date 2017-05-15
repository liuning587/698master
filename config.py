'''config'''
import os
import sys


SOFTWARE_VERSION = 'V5.0Beta1'
SOFTWARE_DT = '2017.05'

TRANS_WINDOW = None
ABOUT_WINDOW = None

GOOD_L = None
GOOD_HCS = None
GOOD_FCS = None

if getattr(sys, 'frozen', False):
    SORTWARE_PATH = sys._MEIPASS
else:
    SORTWARE_PATH = os.path.split(os.path.realpath(__file__))[0]
