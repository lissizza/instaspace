# instaspace/clean.py
import logging
import os
from os.path import isfile
from os.path import join as joinpath

import utils, settings


logger = utils.set_logger('clean')


def clean(args):
    full_clean = args.full_clean
    files = os.listdir(settings.IMAGES_DIR)
    for file in files:
        file_path = joinpath(settings.IMAGES_DIR, file)
        to_delete = 'REMOVE_ME' in file if not full_clean else True
        if not isfile(file_path) or not to_delete:
            continue
        try:
            os.remove(file_path)
        except Exception as e:
            logger.error(str(e))
    logger.info('%s file(s) were deleted.', len(files))


def main():
    clean(utils.get_args())


if __name__ == '__main__':
    main()