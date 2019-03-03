# instaspace/publish_images.py
import argparse
import os
import time
from os.path import isfile
from os.path import join as joinpath

import requests
from dotenv import load_dotenv
from instabot import Bot
from urllib3.exceptions import ProtocolError

import utils, settings


logger = utils.set_logger('Publishing')


def get_images_list_for_publishing():
    return [
        i for i in os.listdir(settings.IMAGES_DIR)
        if isfile(joinpath(settings.IMAGES_DIR, i))
    ]


def publish_images(args: argparse.Namespace) -> None:
    pic_list_for_publishing = get_images_list_for_publishing()
    if not pic_list_for_publishing:
        logger.warning('There are no images to publish.')
        return
    
    logger.info('Start publishing to Instagram.')
    load_dotenv()
    username = os.getenv('LOGIN')
    password = os.getenv('PASSWORD')
    bot = Bot()
    bot.login(username=username, password=password)

    for pic in pic_list_for_publishing:
        caption = pic[:-4]
        try:
            file_path = os.path.join(settings.IMAGES_DIR, pic)
            bot.upload_photo(file_path, caption=caption)
            bot.api.last_response.raise_for_status()
            os.remove(f'{file_path}.CONVERTED.jpg.REMOVE_ME')
            if not args.remove_uploaded:
                uploaded_file_path = os.path.join(settings.UPLOADED_DIR, pic)
                os.rename(file_path, uploaded_file_path)
            else:
                os.remove(file_path)
        except FileNotFoundError as e:
            logger.error('Cannot remove uploaded file: %s', str(e))
        except requests.exceptions.HTTPError as e:
            logger.error(str(e))
        except (ConnectionError, ProtocolError):
            logger.error(
                'Connection aborted, the image %s was not uploaded.',
                caption
            )
        time.sleep(settings.PUBLISHING_TIMEOUT)


def main():
    args = utils.get_args()
    publish_images(args)


if __name__ == '__main__':
    main()