#сценарий 2: показать количество видео в плейлисте
from pymongo import MongoClient


def main():
    pl_id: str = 'PLV6PNz895rnPtiojPsrWAHeUZWMCqPMRT'
    connection: MongoClient = MongoClient('localhost', 27017, connect=False)
    pl_videos = connection[pl_id]['videos']
    pl_videos_len = pl_videos.count_documents({})
    print(f'Количество видео в плейлисте - {pl_videos_len}')
    connection.close()

if __name__ == '__main__':
    main()
