HASH_SIZE = 8192

DB_NAME = 'dupload.db'

STATIC_PATH = '/home/wangdai/static'

FILE_ROOT = STATIC_PATH + '/dupload'

CATEGORY = {
    'imgs': ('.jpg', '.png', '.gif'),
    'doc': ('.txt', '.pdf', '.doc', '.docx', '.xml', '.xls', '.xlsx', '.ppt', '.pptx', '.csv', '.tsv', '.md'),
    'music': ('.mp3',),
    'pack': ('.zip', '.gz', '.bz2', '.tar', '.7z', '.tgz', '.xz')
}

CAT_KEYS = CATEGORY.keys()

PAGE_SIZE = 10

DEBUG = True

