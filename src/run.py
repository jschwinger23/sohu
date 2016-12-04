# coding=utf8

import os
import logging 

from parsing_actor import ParsingActor
from crawling_actor import CrawlingActor
from config import CRAWLING_CONF, PARSING_CONF

def main():
    parsing_thread_num = PARSING_CONF['THREAD_NUM']
    parsing_actor = ParsingActor(thread_num=parsing_thread_num)

    crawling_host = CRAWLING_CONF['HOST']
    crawling_thread_num = CRAWLING_CONF['THREAD_NUM']
    crawling_actor = CrawlingActor(crawling_host, parsing_actor, thread_num=10)
    parsing_actor.crawling_actor = crawling_actor

    crawling_actor.send('/')
    crawling_actor.start()
    parsing_actor.start()

if __name__ == '__main__':
    log_format = '%(asctime)s %(levelname)s %(message)s'
    logfile_path = os.environ['LOG_PATH']
    logfile_name = os.path.join(logfile_path, 'm_sohu.log')
    logging.basicConfig(format=log_format, level=logging.ERROR, filename=logfile_name)
    main()
