from tools import Tools
from loguru import logger
from random import randint


def run():
    """运行每周秘闻副本"""

    tools = Tools()

    for _ in range(1, 11):
        logger.info("任务共 {} 次 | 第 {} 次".format(11, _))
        tools.tap(x=925, y=510, _log="开始，等待任务完成")

        # 寻找准备按钮
        tools.find_img(
            path=tools.paths["zhunbei"],
            x=933, y=472, log="点击准备按钮")

        # 寻找胜利按钮
        tools.find_img(
            path=tools.paths["qianshengli"],
            x=416, y=83, log="点击胜利按钮")

        tools.sleep(randint(2, 5))


if __name__ == "__main__":
    run()
