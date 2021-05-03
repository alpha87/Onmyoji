"""
@Author: Jianxun
@Email: i@lijianxun.top
@File Name: tupo.py
@Description: 结界突破

"""
import sys
from random import choice, shuffle

from loguru import logger

from tools import Tools


class TuPo(object):
    __doc__ = "结界突破。默认每次进攻前失败一次（防止结界突破难度提升）。" \
              "会调用腾讯 AI OCR 接口查询剩余结界券数量。" \
              "请确保阵容是解锁状态。"

    def __init__(self):
        self.tools = Tools()

    @staticmethod
    def shuffle_location():
        """寮结界突破坐标"""

        # 因为攻击胜利会自动补上，所以只需要点第一个位置就可以
        p1 = ((475, 142), (527, 305))
        p2 = ((489, 141), (534, 303))
        p3 = ((531, 138), (512, 302))

        # 随机将上述坐标打乱
        result = [p1, p2, p3, p1, p2, p3]
        shuffle(result)
        return result

    def beat(self, p):
        """进攻操作，包含主动失败退出，正常攻击"""

        # 结界坐标
        x = p[0][0]
        y = p[0][1]

        # 结界对应进攻按钮坐标
        xj = p[1][0]
        yj = p[1][1]

        # 点击结界
        self.tools.tap(x, y, "点击结界")

        # 点击进攻按钮
        while True:
            self.tools.capture_screen()
            match_result = self.tools.match_img(
                capture_img=self.tools.paths["screen"],
                temp_img=self.tools.paths["jingong"]
            )
            if match_result and self.tools.get_pixel(530, 277) != (173, 170, 156):
                self.tools.tap(xj, yj, "点击进攻按钮")
                break
            else:
                logger.warning("冷却时间未到")
                self.tools.tap(x, y)
                sys.exit(0)
            self.tools.sleep(1)

        # 开始后点击 4 号式神
        click_list = [(662, 314), (659, 333), (658, 352)]
        while True:
            self.tools.capture_screen()
            self.tools.sleep(0.2)
            c = self.tools.get_pixel(431, 568)
            if c == (255, 255, 255):
                x, y = choice(click_list)
                self.tools.tap(x, y, "点击茨林")
                break
            self.tools.sleep(1)

        # 寻找胜利图标
        self.tools.find_img(
            path=self.tools.paths["shengli"],
            x=501, y=436, log="胜利")

    def run(self):
        n = 0
        logger.warning("数据库无数据，默认使用本地坐标")
        loc_list = self.shuffle_location()

        for loc in loc_list:
            n += 1
            self.tools.sleep(1)
            logger.info("第{}次突破".format(n))
            self.beat(loc)

            if n == 6:
                break


if __name__ == "__main__":
    t = TuPo()
    t.run()
