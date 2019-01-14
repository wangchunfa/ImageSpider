# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import requests
import random
from ImageSpider.settings import IMAGES_STORE, COOKIE

uapools = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]


class ImagespiderPipeline(object):

    def process_item(self, item, spider):
        fold_name = "".join(item['title'])
        header = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                   'Accept-Encoding': 'gzip, deflate',
                   'Accept-Language': 'zh-CN,zh;q=0.8',
                   'Cache-Control': 'no-cache',
                   'Connection': 'keep-alive',
                   'Cookie': 'UM_distinctid=15fa02251e679e-05c01fdf7965e7-5848211c-144000-15fa02251e7800; bdshare_firstime=1510220189357; CNZZDATA1263415983=1653134122-1510216223-null%7C1510216223; CNZZDATA3866066=cnzz_eid%3D376479854-1494676185-%26ntime%3D1494676185; Hm_lvt_9a737a8572f89206db6e9c301695b55a=1510220189; Hm_lpvt_9a737a8572f89206db6e9c301695b55a=1510220990',
                   'Host': 'img1.mm131.me',
                   'Pragma': 'no-cache',
                   'Referer': 'http://www.mm131.com/xinggan/',
                   'User-Agent': random.choice(uapools)}

        images = []
        # 所有图片放在一个文件夹下
        dir_path = '{}'.format(IMAGES_STORE)
        if not os.path.exists(dir_path) and len(item['src']) != 0:
            os.mkdir(dir_path)

        for jpg_url, name in zip(item['src'], item['alt']):
            file_name = name
            file_path = '{}//{}'.format(dir_path, file_name)
            images.append(file_path)
            if os.path.exists(file_path) or os.path.exists(file_name):
                continue

            print(jpg_url)
            with open('{}//{}.jpg'.format(dir_path, file_name), 'wb') as f:
                req = requests.get(jpg_url, headers=header, timeout=10)
                f.write(req.content)

        return item

