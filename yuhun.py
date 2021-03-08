from tools import Tools
from loguru import logger
from random import randint


def run(number):
    """运行"""

    tools = Tools()

    for _ in range(1, number + 1):

        logger.info("任务共 {} 次 | 第 {} 次".format(number, _))
        tools.tap(x=925, y=510, _log="开始，等待任务完成")

        while True:
            tools.capture_screen()
            match_result = tools.match_img(
                capture_img=tools.paths["screen"],
                temp_img=tools.paths["shengli"]
            )
            if match_result:
                tools.tap(700, 400, "胜利！\n")
                tools.sleep(randint(2, 5))
                break
            tools.sleep(3)


if __name__ == "__main__":
    run(int(input("次数：")))
