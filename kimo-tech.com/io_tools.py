import json
import os
import requests
import time
from multiprocessing import Process, Queue, Pool
import threading
from contextlib import closing

defult_headers = {
'Host': 'www.rainier.net.cn',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
'Accept-Encoding': 'gzip, deflate',
'Cookie': 'Hm_lvt_4042b9906bee689ae3639dabd531701c=1517062756,1517103439,1517117370,1517145240;\
 Hm_lvt_7787f2e38247c6dfbc87f7fe374c1aaf=1517062756,1517103441,1517117370,1517145240; JSESSIONID=673775564DF1278C411CED1D4A4FFEF1; Hm_lpvt_7787f2e38247c6dfbc87f7fe374c1aaf=1517145657; Hm_lpvt_4042b9906bee689ae3639dabd531701c=1517145657',
'Connection': 'keep-alive',
}

# 将页面信息转换为json 字符串并保存到本地文件
def add_to_file(file_path, data):
    """ 保存某页面的信息 """
    txt = json.dumps(data)
    with open(file_path, 'a') as f:
        f.write(txt)
        f.write('\n')


# 初始化文件夹
def setup_download_dir(directory):
    # 设置文件夹，文件夹名为传入的 directory 参数，若不存在会自动创建 """
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except Exception as e:
            print(e)
    return True
    pass


class ProgressBar(object):
    def __init__(self, title,
                 count=0.0,
                 run_status=None,
                 fin_status=None,
                 total=100.0,
                 unit='', sep='/'):
        super(ProgressBar, self).__init__()
        self.info = "【%s】%s %.2f %s %s %.2f %s"
        self.title = title
        self.total = total
        self.count = count
        self.status = run_status or ""
        self.fin_status = fin_status or " " * len(self.status)
        self.unit = unit
        self.seq = sep

    def __get_info(self):
        # 【名称】状态 进度 单位 分割线 总数 单位
        _info = self.info % (self.title, self.status,
                             self.count/1024, self.unit, self.seq, self.total/1024, self.unit)
        return _info

    def refresh(self, count=1, status=None):
        self.count += count
        # if status is not None:
        self.status = status or self.status
        end_str = "\r"
        if self.count >= self.total:
            end_str = '\n'
            self.status = status or self.fin_status
        print(self.__get_info() + end_str)
        # , end=end_str


# 下载器
class Downland:

    def __init__(self, headers):
        if headers == None:
            headers = defult_headers
        self.headers = headers
        self.queue = None

    def download_one(self, img):
        """ 下载一张图片 """
        url, directory, filepath = img
        # 如果文件已经存在，放弃下载
        if os.path.exists(filepath):
            print('exists:', filepath)
            return
        setup_download_dir(directory)
        print('start download', url)
        rsp = requests.get(url, headers=self.headers)
        with open(filepath, 'wb') as f:
            f.write(rsp.content)
            print('end download', url)

    def downland_one_with_progress(self, img):
        url, directory, filepath = img
        # 如果文件已经存在，放弃下载
        if os.path.exists(filepath):
            print('exists:', filepath)
            return
        setup_download_dir(directory)
        print('start download', url)
        with closing(requests.get(url, headers=self.headers, stream=True)) as response:
            chunk_size = 1024000  # 单次请求最大值
            content_size = int(response.headers['content-length'])  # 内容体总大小
            progress = ProgressBar(filepath, total=content_size,
                                   unit="KB", run_status="正在下载", fin_status="下载完成")
            with open(filepath, "wb") as file:
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)
                    progress.refresh(count=len(data))
        print('end download', url)

    def begin_thread(self, threading_count=4):
        print('开始多线程下载')
        self.queue = Queue()
        for i in range(threading_count):
            w = threading.Thread(target=self.thread_down_img, args=(self.queue,))
            w.setDaemon(True)
            w.start()
        pass

    def stop_thread(self):
        # self.queue.task_done()
        self.queue.close()
        print('完成多线程下载')
        pass

    def thread_downland(self, img):
        self.queue.put(img)
        pass

    def thread_down_img(self, q):
        while True:
            if not q.empty():
                img = q.get()
                self.downland_one_with_progress(img)
                time.sleep(1)
            # q.task_done()
        pass

    def download_many(self, imgs, processes=10):
        """ 并发下载所有图片 """
        start_time = time.time()
        pool = Pool(processes)
        for img in imgs:
            pool.apply_async(self.download_one, (img,))

        pool.close()
        pool.join()
        end_time = time.time()
        print('下载完毕,用时:%s秒' % (end_time - start_time))


if __name__ == '__main__':
    downland = Downland()