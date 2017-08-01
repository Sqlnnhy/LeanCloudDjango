# -*- coding:utf-8 -*-
import os
import leancloud
from gevent.pywsgi import WSGIServer
from cloud import engine
from gevent import monkey
monkey.patch_all()


# 设置 Django 项目配置文件
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LeanCloudDjango.settings")

APP_ID = os.environ['LEANCLOUD_APP_ID']
APP_KEY = os.environ['LEANCLOUD_APP_KEY']
MASTER_KEY = os.environ['LEANCLOUD_APP_MASTER_KEY']
PORT = int(os.environ['LEANCLOUD_APP_PORT'])

leancloud.init(APP_ID, master_key=MASTER_KEY)

application = engine

if __name__ == '__main__':
    # 只在本地开发环境执行的代码
    server = WSGIServer(('localhost', PORT), application)
    server.serve_forever()
