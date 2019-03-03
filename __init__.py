# instaspace/__init__.py
from instaspace import utils, settings


utils.ensure_dir(settings.IMAGES_DIR)
utils.ensure_dir(settings.UPLOADED_DIR)