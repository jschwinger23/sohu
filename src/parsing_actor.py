# coding=utf8

import urllib
import logging
import threading

from lxml import html

from actor import Actor

class ParsingActor(Actor):
    '''
    解析html的Actor
    通过xpath解析出html中href属性里的m.sohu.com的路径
    切分查询、标签，去重检验
    发送至crawling_actor进行页面抓取
    '''

    def __init__(self, thread_num=1):
        self.thread_num = thread_num
        self.xpath = '//*[starts-with(@href, "/")]/@href'
        super(ParsingActor, self).__init__()

        self.path_pool = set()
        self.path_pool_lock = threading.Lock()

    def _bootstrap(self, task):
        try:
            dom_root = html.fromstring(task)

        except:
            message = '{task} [Unknown Error within parsing html'.format(task=task)
            logging.error(message)
            return

        paths = dom_root.xpath(self.xpath)
        if not paths:
            return

        for path in paths:
            path = self._encode(path)
            path = self._normal(path)
            if self._is_checked(path):
                continue 

            self.crawling_actor.send(path)

    def _encode(self, path):
        if not isinstance(path, unicode):
            return path

        encodings = ['utf8', 'gbk', 'raw-unicode-escape']
        for encoding in encodings:
            try:
                return path.encode(encoding)
            except UnicodeEncodeError:
                continue

        raise NotImplementedError

    def _normal(self, path):
        path, _ = urllib.splittag(path)
        path, _ = urllib.splitquery(path)
        return path

    def _is_checked(self, path):
        with self.path_pool_lock:
            if path in self.path_pool:
                return True

            self.path_pool.add(path)
            return False

