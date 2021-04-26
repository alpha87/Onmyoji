"""
@Author: Jianxun
@Email: i@lijianxun.top
@File Name: miwen.py
@Description: 每周秘闻副本。默认从第一次开始，共十次。

"""

from random import randint
from threading import Thread

from loguru import logger

from tools import Tools


class MiWen:
    """运行每周秘闻副本"""

    def __init__(self):
        self.tools = Tools()

    def find_zhunbei(self):
        """寻找准备按钮"""

        self.tools.find_img(
            path=self.tools.paths["zhunbei"],
            x=933, y=472, log="点击准备按钮")

    def find_qianshengli(self):
        """寻找胜利标志"""

        self.tools.find_img(
            path=self.tools.paths["qianshengli"],
            x=416, y=83, log="点击胜利按钮",
            thread_flag=True)

    def find_shengli(self):
        """寻找胜利标志（达摩蛋）"""
        self.tools.find_img(
            path=self.tools.paths["shengli"],
            x=416, y=83, log="点击胜利（达摩蛋）按钮",
            thread_flag=True)

    def run(self):
        for _ in range(1, 11):
            logger.info("任务共 {} 次 | 第 {} 次".format(11, _))
            self.tools.tap(x=925, y=510, _log="开始，等待任务完成")

            self.find_zhunbei()

            t1 = Thread(target=self.find_shengli)
            t2 = Thread(target=self.find_qianshengli)
            t1.start()
            t2.start()
            t1.join()
            t2.join()

            self.tools.sleep(randint(1, 5))


if __name__ == "__main__":
    m = MiWen()
    m.run()
