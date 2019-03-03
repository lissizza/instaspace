# instaspace/settings.py

# Common settings section
IMAGES_DIR = 'images/'
UPLOADED_DIR = 'images/uploaded/'
LOGFILE_NAME = 'instaspace.log'

# Hubble settings section
HUBBLE_API_URL = 'http://hubblesite.org/api/v3/'
MAX_IMAGE_BYTES_SIZE = 3000000  # bytes
DEFAULT_MISSION = 'latest'

# SpaceX settings section
SPACEX_API_URL = 'https://api.spacexdata.com/v3/launches/'
DEFAULT_COLLECTION = 'news'

# Publishing settings section
PUBLISHING_TIMEOUT = 20  # seconds
