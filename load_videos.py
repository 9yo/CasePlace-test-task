from requests import get
from json import loads
from pymongo import MongoClient

from key import api_private_key


def get_all_videos_from_playlist(pl_id):
    link: str =  f'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId={pl_id}&maxResults=50&key={api_private_key}'
    response = get(link)

    #if response.status_code != 200:
    #    print('Request Error!')
    #    return

    pl_data = loads(response.text)
    pl_next_page_token = pl_data.get('nextPageToken')
    vids: list = pl_data['items']

    while pl_next_page_token:
        response = get(link + f'&pageToken={pl_next_page_token}')
        pl_data = loads(response.text)
        pl_next_page_token = pl_data.get('nextPageToken')
        vids += pl_data['items']

    return vids

def save_videos_to_db(pl_id, videos):
    connection: MongoClient = MongoClient('localhost', 27017, connect=False)
    pl_videos = connection[pl_id]['videos']
    pl_videos.insert_many(videos)
    connection.close()

def setup_db(pl_id):
    connection: MongoClient = MongoClient('localhost', 27017, connect=False)
    pl_videos = connection[pl_id]['videos']

    if len(list(pl_videos.find({}))) != 0:
        print('Seems like the playlist is already loaded!\nOverwriting..')
        pl_videos.drop()

    connection.close()


def main():
    pl_id: str = 'PLV6PNz895rnPtiojPsrWAHeUZWMCqPMRT'
    setup_db(pl_id)
    vids = get_all_videos_from_playlist(pl_id)
    print('{} videos loaded!'.format(len(vids)))
    save_videos_to_db(pl_id, vids)
    print('Saved used Mongo by key - {}'.format(pl_id))


if __name__ == '__main__':
    main()
