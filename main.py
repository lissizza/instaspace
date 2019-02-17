import os
import requests


IMAGES_DIR = 'images/'
HUBBLE_API_URL = 'http://hubblesite.org/api/v3'


def ensure_dir(file_path:str) -> None:
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)


def save_image(image_url:str, image_name:str) -> None:
    response = requests.get(image_url)
    with open(image_name, 'wb') as file:
        file.write(response.content)


def get_image_extension(image_url:str) -> str:
    if '.' in image_url:
        return image_url.split('.')[-1]
    return ''


def fetch_spacex_last_launch() -> None:
    latest_launch_api_url = 'https://api.spacexdata.com/v3/launches/latest'
    response = requests.get(latest_launch_api_url)
    response.raise_for_status()
    try:
        image_urls = response.json()['links']['flickr_images']
    except KeyError:
        image_urls = []
    for image_url in image_urls:
        image_name = image_url.split('/')[-1]
        image_path = os.path.join(IMAGES_DIR, image_name)
        save_image(image_url, image_path)


def fetch_hubble_image_by_id(image_id:int):
    hubble_single_image_api_url = f'{HUBBLE_API_URL}/image/{image_id}'
    response = requests.get(hubble_single_image_api_url)
    response.raise_for_status()
    try:
        image_url = response.json()['image_files'][-1]['file_url']
        image_extension = get_image_extension(image_url)
        image_name = f'{image_id}.{image_extension}'
        image_path = os.path.join(IMAGES_DIR, image_name)
        save_image(image_url, image_path)
    except KeyError:
        raise KeyError(f'Cannot get image {image_id} from the response.')


def fetch_images_from_collection(collection:str) -> None:
    hubble_all_images_api_url = f'{HUBBLE_API_URL}/images/{collection}'
    response = requests.get(hubble_all_images_api_url)
    response.raise_for_status()
    image_ids = [item['id'] for item in response.json()]
    print('{len(image_ids)} found in the collection "{collection}".')
    for image_id in image_ids:
        try:
            print(f'Start downloading image {image_id}.')
            fetch_hubble_image_by_id(image_id)
            print(f'Image {image_id} is fetched.')
        except (requests.exceptions.HTTPError, KeyError) as e:
            print(str(e))
            continue
    print('Downloading is finished.')


def main():
    ensure_dir(IMAGES_DIR)
    fetch_spacex_last_launch(images_dir)
    collection = 'news'
    try:
        fetch_images_from_collection(collection)
    except (requests.exceptions.HTTPError, KeyError) as e:
        print(f'Cannot access Hubble: {str(e)}')


if __name__ == '__main__':
    main()
