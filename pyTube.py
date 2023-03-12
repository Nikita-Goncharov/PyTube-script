import logging
import os

import validators
from pytube import YouTube, Playlist

FORMAT = '[%(asctime)s] %(filename)s[LINE:%(lineno)d] %(levelname)-8s  %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)

# TODO: more adaptive
# linux
DEFAULT_DOWNLOAD_BASE_DIR = '/home/nikita-goncharov/Downloads'

"""
TODO: 
3. Download path(default-folder Downloads)
4. Add logging

"""


def get_single(single_streams, instanse_type):
    if instanse_type == 'v':
        instanse = single_streams.filter(type='video').filter(progressive=True).order_by('itag').desc().first()
        logging.info(f'Downloaded video: {instanse}')
    elif instanse_type == 'a':
        instanse = single_streams.filter(type='audio').order_by('itag').desc().first()
        logging.info(f'Downloaded audio: {instanse} - {instanse.title}')

    return instanse


# TODO: if video/audio already exists - just skip

def single_download(instanse_type, url):
    single = YouTube(url)
    single = get_single(single.streams, instanse_type=instanse_type)
    single.download(output_path=DEFAULT_DOWNLOAD_BASE_DIR)


def playlist_download(instanse_type, url):
    playlist = Playlist(url)
    for single in playlist.videos:
        single = get_single(single.streams, instanse_type=instanse_type)
        single.download(output_path=DEFAULT_DOWNLOAD_BASE_DIR)


def download(instanse_type, amount, url):
    if amount == 's':
        single_download(instanse_type=instanse_type, url=url)
    elif amount == 'p':
        playlist_download(instanse_type=instanse_type, url=url)


def main():
    while True:
        video_or_audio = input("Video[v] or Audio[a]: ")
        single_or_playlist = input("Single[s] or Playlist[p]: ")

        if video_or_audio in ['v', 'a'] and single_or_playlist in ['s', 'p']:
            break
        else:
            logging.error('Write chars from the proposed')

    while True:
        path_for_download = input(f"Path for downloading(default={DEFAULT_DOWNLOAD_BASE_DIR}): ")

        if path_for_download == '' or os.path.exists(path_for_download):
            break
        else:
            logging.error('Path does not exists')

    while True:
        url = input("Link: ")
        if validators.url(url):
            break
        else:
            logging.error('Url is not valid')

    download(instanse_type=video_or_audio, amount=single_or_playlist, url=url)


if __name__ == '__main__':
    main()
