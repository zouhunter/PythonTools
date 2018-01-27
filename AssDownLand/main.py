import downland_holders
import html_info
import ass_core


# 下载
def main():
    imgs = ass_core.get_info_imgs()
    head = html_info.Head("header.txt")
    downland_holder = downland_holders.Downland(head.headers)
    downland_holder.download_many(imgs)

if __name__ == '__main__':
    main()
