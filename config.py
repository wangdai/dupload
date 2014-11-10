HASH_SIZE = 4096

DB_NAME = 'dupload.db'

STATIC_PATH = '/home/wangdai/static'

FILE_ROOT = STATIC_PATH + '/dupload'

CATEGORY = {
    'img'  : ('.jpg', '.png', '.gif'),
    'doc'  : ('.txt', '.pdf', '.doc', '.docx', '.xml', '.xls', '.xlsx', '.ppt', '.pptx', '.csv', '.tsv'),
    'music': ('.mp3',),
    'pack' : ('.zip', '.gz', '.bz2', '.tar', '.7z', '.md')
}

PAGE_SIZE = 10
