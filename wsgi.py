# -*- coding:utf-8 -*-
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LeanCloudDjango.settings")

import leancloud
from gevent.pywsgi import WSGIServer
from cloud import engine
from gevent import monkey
monkey.patch_all()

""" online
APP_ID = os.environ['LEANCLOUD_APP_ID']
APP_KEY = os.environ['LEANCLOUD_APP_KEY']
MASTER_KEY = os.environ['LEANCLOUD_APP_MASTER_KEY']
PORT = int(os.environ['LEANCLOUD_APP_PORT'])
"""

# localhost
APP_ID = '7sP73D83PYWsCcJVlLDlQUnJ-gzGzoHsz'
APP_KEY = 'qf16kTDRWbO3KnnTR8y1eYlb'
MASTER_KEY = 'pkpqn2JuA75Qe16Aos4fH847'
PORT = 8000


leancloud.init(APP_ID, master_key=MASTER_KEY)

application = engine

if __name__ == '__main__':
    # 只在本地开发环境执行的代码
    server = WSGIServer(('localhost', PORT), application)
    server.serve_forever()
