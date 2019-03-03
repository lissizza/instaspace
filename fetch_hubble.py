# instaspace/fetch_hubble.py
import argparse

import requests

import utils, settings


logger = utils.set_logger('Hubble')


def get_max_fit_hubble_image(images_files: dict) -> str:
    """
    Get a pic of the max quality but not exceeding of the size limit.
    """
    image_url = ''
    for image in images_files[::-1]:
        if image['file_size'] < settings.MAX_IMAGE_BYTES_SIZE:
            image_url = image['file_url']
            break

    return image_url


def get_image_url_and_path_by_id(image_id: int) -> (str, str):
    hubble_single_image_api_url = f'{settings.HUBBLE_API_URL}image/{image_id}'
    response = requests.get(hubble_single_image_api_url)
    response.raise_for_status()

    response_dict = response.json()
    image_url = get_max_fit_hubble_image(response_dict['image_files'])
    image_path = utils.get_image_path(
        response_dict['name'],
        image_url,
        image_id
    )

    return image_url, image_path


def get_collection_images_ids_and_names(collection: str) -> list:
    hubble_all_images_api_url = f'{settings.HUBBLE_API_URL}images/{collection}'
    response = requests.get(hubble_all_images_api_url)
    response.raise_for_status()

    return [(item['id'], item['name']) for item in response.json()]


def fetch_hubble(args: argparse.Namespace) -> None:
    collection = args.hubble_collection
    try:
        image_data = get_collection_images_ids_and_names(collection)
    except Exception as e:
        logger.error(
            'An error occured, Hubble images data cannot be retrieved: %s',
            str(e)
        )
        return

    if not image_data:
        logger.warning(
            'Images data on the Hubble site is empty. Try another collection.'
        )
        return

    logger.info('Start Hubble downloading.')
    logger.info(
        '%i Hubble pics found in the collection "%s".',
        len(image_data),
        collection
    )
    for image_id, image_name in image_data:
        try:
            image_url, image_path = get_image_url_and_path_by_id(image_id)
            if not image_url:
                logger.info(
                    '%i: An appropriate image was not found.',
                    image_id
                )
                continue
            logger.info('Downloading image %s from %s.', image_name, image_url)
            is_downloaded = utils.download_image(image_url, image_path)
        except Exception as e:
            logger.error(
                'Error occured, the image %s was not downloaded: %s',
                image_name,
                str(e)
            )
            continue
        if is_downloaded:
            logger.info('Image %s saved.', image_name)
        else:
            logger.info(
                'Image with name %s already exists, skipped.',
                image_name
            )
    logger.info('Hubble downloading is finished.')


def main():
    args = utils.get_args()
    fetch_hubble(args)


if __name__ == '__main__':
    main()
