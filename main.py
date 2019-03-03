# instaspace/main.py
import utils
from fetch_hubble import fetch_hubble
from fetch_spacex import fetch_spacex
from publish_images import publish_images
from clean import clean


def main():
    args = utils.get_args()
    if not args.upload_only:
        fetch_spacex(args)
        fetch_hubble(args)
    if not args.download_only:
        publish_images(args)
    clean(args)


if __name__ == '__main__':
    main()
