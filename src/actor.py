# coding=utf8

import time
import Queue
import threading

class Actor(object):
    '''
    Actor模式基类
    对外调用send方法将任务加入队列，内部线程取出任务调用_bootstrap方法
    派生的子类需要复写_bootstrap方法
    '''
    
    def __init__(self, *args, **kws):
        self._task_q = Queue.Queue()

    def send(self, task):
        self._task_q.put(task)

    def start(self):
        self.thread_pool = []
        for i in xrange(self.thread_num):
            thread_obj = threading.Thread(target=self.run, args=(self._task_q,), name=str(i))
            self.thread_pool.append(thread_obj)
            thread_obj.start()

    def run(self, task_q):
        while True:
            try:
                task = task_q.get(timeout=10)
            
            except Queue.Empty:
                break

            else:
                print 'task_q in %s remains %s' % (type(self).__name__, task_q.qsize())
                self._bootstrap(task)
                

    def _bootstrap(self, task):
        raise NotImplementedError
