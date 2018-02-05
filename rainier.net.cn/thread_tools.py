import threading
from multiprocessing import Queue


class Job(object):
    def __init__(self, priority, description):
        self.priority = priority
        self.description = description
        print('Job:', description)
        return


def process_job(q):
    while not q.empty():
        next_job = q.get()
        print('for:', next_job.description)
        q.task_done()

if __name__ == '__main__':
    q = Queue()

    q.put(Job(3, 'level 3 job'))
    q.put(Job(10, 'level 10 job'))
    q.put(Job(1, 'level 1 job'))

    for i in range(2):
        w = threading.Thread(target=process_job, args=(q,))
        w.setDaemon(True)
        w.start()

    q.put(Job(10, 'level 10 job'))
    q.put(Job(1, 'level 1 job'))
