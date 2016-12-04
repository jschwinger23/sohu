# coding=utf8

import logging
import threading

import requests

from actor import Actor

class CrawlingActor(Actor):
    '''
    html抓取的actor
    使用requests模块进行抓取并捕捉异常
    得到的html发送至parsing_actor进行清洗
    '''

    def __init__(self, host, parsing_actor, thread_num=1):
        self.host = host
        self.thread_num = thread_num
        self.parsing_actor = parsing_actor
        super(CrawlingActor, self).__init__()

    def _bootstrap(self, task):
        url = self.host + task

        try:
            resp = requests.get(url)
            resp.raise_for_status()

        except requests.ConnectionError:
            message = '{url} [ConnectionError]'.format(url=task)

        except requests.HTTPError as e:
            message = '{url} [Unsuccessful status_code {status_code}]'.format(url=task, status_code=e.response.status_code)
            
        except requests.Timeout:
            message = '{url} [Request timeout]'.format(url=task)

        except requests.TooManyRedirects:
            message = '{url} [Redirection Limit Exceeded]'.format(url=task)

        except requests.exceptions.RequestException:
            message = '{url} [Unknown Error within fetching html]'.format(url=task)

        else:
            # 没有异常的情况下就会运行到这里，向parsing_actor发送新任务
            message = '{task} [ok]'.format(task=task)
            logging.info(message)
            self.parsing_actor.send(resp.content)
            return

        logging.error(message)
