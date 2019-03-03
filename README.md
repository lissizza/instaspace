# Space Instagram

This project is intended to get photos from open [SpaceX](https://www.spacex.com/) and [Hubble](http://hubblesite.org/) sources and publish them automatically to your [Instagram](https://www.instagram.com) account.

### How to install

To start automatically downloading and publishing you need to create `.env` file in the root project folder and save there your Instagram account login and password using the next format:

```.env
LOGIN=your_instagram_login
PASSWORD=your_instagram_password
```
 
Python3 should be already installed. The minimum requirement is Python 3.6.
Use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```

### How to use
Run the main script:
```
$ python3 main.py 
```
By default this script get photos of the last SpaceX launch and from the "news" Hubble collection.

You can change the collection name and a SpaceX mission number at will. 
Try `./main.py --help` to see possible collection names and other options.  


### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).

### TODO:
* Add an ability to get photos from SpaceX by a mission date or mission name (hard to find mission numbers).