import os

# should probably put this key outside of repo
SECRET_KEY = 'dX6t*g7ZG@_RcDTigd*!r8@K4KaQer4L'
DEBUG = True

MANAGERITM_CLIENT_COMMAND = ['sleep', '10000000000000']
MANAGERITM_LOG_DIR = os.getcwd()
MANAGERITM_PROXY_HARS_DIR = "./hars"
MANAGERITM_PROXY_PORT_LOWER_BOUND = 5200
MANAGERITM_PROXY_PORT_UPPER_BOUND = 5299
