# сценарий 1: показать названия трех самых последних видео плейлист
from pymongo import MongoClient


def main():
    pl_id: str = 'PLV6PNz895rnPtiojPsrWAHeUZWMCqPMRT'
    connection: MongoClient = MongoClient('localhost', 27017, connect=False)
    pl_videos = connection[pl_id]['videos']
    print('Последние три видео плейлиста:\n')
    for el in list(pl_videos.find({}))[-3:]:
        print(el['snippet']['title'])

    connection.close()

if __name__ == '__main__':
    main()
