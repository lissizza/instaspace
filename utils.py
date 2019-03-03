# instaspace/utils.py
import argparse
import logging
import os
import unicodedata

import requests

import settings


def ensure_dir(file_path: str) -> None:
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)


def download_image(image_url: str, image_name: str) -> bool:
    if os.path.isfile(image_name):
        return False
    response = requests.get(image_url)
    response.raise_for_status()
    with open(image_name, 'wb') as file:
        file.write(response.content)
    return True


def clean_image_name(raw_image_name: str) -> str:
    image_name = unicodedata.normalize(
        'NFKD', raw_image_name
    ).encode('ascii', 'ignore')
    name_list = image_name.decode('utf-8').split('/ ')
    return ' '.join([word.strip() for word in name_list])[:255]


def get_image_extension(image_url: str) -> str:
    return os.path.splitext(image_url)[-1]


def get_image_path(filename: str, image_url: str, i:int) -> str:
    image_extension = get_image_extension(image_url)
    image_name = clean_image_name(filename)
    image_full_name = f'{image_name} {str(i)}{image_extension}'

    return os.path.join(settings.IMAGES_DIR, image_full_name)


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Fetch images from SpaceX and Hubble API and publish them '
                    'to the Instagram.',
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        '--upload_only',
        required=False,
        action='store_true',
        help='''
                Don\'t fetch images, publish only.
            '''
    )
    parser.add_argument(
        '--download_only',
        required=False,
        action='store_true',
        help='''
                Don\'t publish images, download only.
            '''
    )
    parser.add_argument(
        '--remove_uploaded',
        required=False,
        action='store_true',
        help='''
                Delete uploaded files instead to copy them
                to uploaded dir.
            '''
    )
    parser.add_argument(
        '--full_clean',
        required=False,
        action='store_true',
        help='''
                Delete all files from the image folder.
            '''
    )
    parser.add_argument(
        '--hubble_collection',
        required=False,
        default=settings.DEFAULT_COLLECTION,
        help=f'''
                Name of image collection on Hubble. 
                The default collection is "{settings.DEFAULT_COLLECTION}".
                Available collections:
                * all
                * news
                * spacecraft
                * printshop
                * holiday_cards
                * stsci_gallery
                * wallpaper
        '''
    )
    parser.add_argument(
        '--spacex_mission',
        required=False,
        default=settings.DEFAULT_MISSION,
        help=f'''
                Number of a mission on SpaceX. 
                By default get the {settings.DEFAULT_MISSION} mission.
            '''
    )
    args = parser.parse_args()
    return args


def set_logger(module_name):
    logging.basicConfig(
        level=logging.INFO,
        datefmt='%d.%m.%y %H:%M'
    )
    logger = logging.getLogger(module_name)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s: %(message)s'
    )
    file_logger = logging.FileHandler(settings.LOGFILE_NAME)
    file_logger.setFormatter(formatter)
    logger.addHandler(file_logger)

    return logger
