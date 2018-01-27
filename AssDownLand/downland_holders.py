import os
import requests
import time
from multiprocessing import Process, Queue, Pool


# 下载器
class Downland:

    def __init__(self, headers):
        self.headers = headers

    def download_one(self, img):
        """ 下载一张图片 """
        url, directory, filepath = img
        # 如果文件已经存在，放弃下载
        if os.path.exists(filepath):
            print('exists:', filepath)
            return
        Downland.setup_download_dir(directory)
        rsp = requests.get(url, headers=self.headers)
        print('start download', url)
        with open(filepath, 'wb') as f:
            f.write(rsp.content)
            print('end download', url)

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

    @staticmethod  # 初始化文件夹
    def setup_download_dir(directory):
        # 设置文件夹，文件夹名为传入的 directory 参数，若不存在会自动创建 """
        if not os.path.exists(directory):
            try:
                os.makedirs(directory)
            except Exception as e:
                print(e)
        return True
        pass


if __name__ == '__main__':
    downland = Downland()