HASH_SIZE = 8192

DB_NAME = 'dupload.db'

STATIC_PATH = '/home/wangdai/static'

FILE_ROOT = STATIC_PATH + '/dupload'

CATEGORY = {
    'imgs': ('.jpg', '.png', '.gif', '.svg'),
    'doc': ('.txt', '.pdf', '.doc', '.docx', '.xml', '.xls', '.xlsx', '.ppt', '.pptx', '.csv', '.tsv', '.md'),
    'music': ('.mp3', '.aac', '.flac'),
    'pack': ('.zip', '.tar', 'tar.bz2', '.tar.gz', '.7z', '.tgz', '.tar.xz', '.rar')
}

CAT_KEYS = CATEGORY.keys()

PAGE_SIZE = 10

DEBUG = True

