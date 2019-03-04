# instaspace/fetch_spacex.py
import requests

import utils, settings


logger = utils.set_logger('SpaceX')


def get_mission_name_and_images_urls(mission) -> (str, list):
    latest_launch_api_url = f'{settings.SPACEX_API_URL}{mission}'
    response = requests.get(latest_launch_api_url)
    response.raise_for_status()
    response_dict = response.json()
    try:
        images_urls = response_dict['links']['flickr_images']
    except KeyError:
        images_urls = []
    mission_name = response_dict.get('mission_name', '')

    return mission_name, images_urls


def fetch_spacex(args) -> None:
    mission = args.spacex_mission
    try:
        mission_name, images_urls = get_mission_name_and_images_urls(mission)
    except Exception as e:
        logger.error(
            'An error is occurred, SpaceX images data cannot be retrieved: %s',
            str(e)
        )
        return

    if not images_urls:
        logger.warning(
            'Images data on the SpaceX site is empty. Try another mission.'
        )
        return

    logger.info('Start downloading SpaceX.')
    logger.info('%i SpaceX images found.', len(images_urls))
    for i, image_url in enumerate(images_urls):
        image_path = utils.get_image_path(mission_name, image_url, i)
        logger.info(f'Downloading image %s.', image_url)
        try:
            is_downloaded = utils.download_image(image_url, image_path)
        except Exception as e:
            logger.error(
                'Image %s cannot be retrieved: %s',
                image_path,
                str(e)
            )
            continue
        if is_downloaded:
            logger.info('%s is fetched.', image_url)
        else:
            logger.warning('Skip %s.', image_url)
    logger.info('SpaceX downloading is finished.')


def main():
    fetch_spacex(utils.get_args())


if __name__ == '__main__':
    main()
