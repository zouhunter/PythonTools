# 专门解析头部信息
class Head:
    @property
    def headers(self):
        return self._headers

    # 初始化
    def __init__(self, file_name):
        self._headers = {}  # 初始化cookies字典变量
        f = open(file_name, 'r')  # 打开所保存的cookies内容文件
        for line in f.read().split('\n'):  # 按照字符：进行划分读取
            # 其设置为1就会把字符串拆分成2份
            name, value = line.strip().split(': ', 1)
            self._headers[name] = value  # 为字典cookies添加内容


if __name__ == '__main__':
    head = Head('header.txt')
    print(head.headers)
