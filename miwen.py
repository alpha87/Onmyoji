"""
@Author: Jianxun
@Email: i@lijianxun.top
@File Name: miwen.py
@Description: 每周秘闻副本。默认从第一层开始，共十层。

"""
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

    def run(self):
        for _ in range(1, 11):
            logger.info("秘闻副本共 {} 层 | 当前第 {} 层".format(11, _))
            self.tools.tap(x=925, y=510, _log="开始，等待任务完成")
            self.find_zhunbei()
            self.tools.find_img_miwen(
                paths=[self.tools.paths["shengli"],
                       self.tools.paths["qianshengli"]],
                x=416, y=83, log="点击胜利按钮")


if __name__ == "__main__":
    m = MiWen()
    m.run()
