"""
@Author: Jianxun
@Email: i@lijianxun.top
@File Name: tupo.py
@Description: 结界突破

"""

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
        """结界突破九宫格坐标"""

        # 第一个元组是结界按钮，第二个元组是对应进攻按钮
        p1 = ((275, 138), (307, 309))
        p2 = ((546, 141), (574, 309))
        p3 = ((810, 143), (839, 310))
        p4 = ((287, 251), (306, 415))
        p5 = ((553, 254), (574, 419))
        p6 = ((821, 255), (840, 417))
        p7 = ((284, 360), (307, 526))
        p8 = ((538, 361), (573, 526))
        p9 = ((807, 362), (838, 528))

        # 随机将上述坐标打乱
        result = [p1, p2, p3, p4, p5, p6, p7, p8, p9]
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

        num = 2  # 进攻次数 2 次
        n = 0

        for _ in range(num):

            # 点击结界
            self.tools.tap(x, y, "点击结界")

            # 点击进攻按钮
            self.tools.tap(xj, yj, "点击进攻按钮")

            if n == 0:
                # 寻找退出按钮
                while True:
                    self.tools.capture_screen()
                    match_result = self.tools.match_img(
                        capture_img=self.tools.paths["screen"],
                        temp_img=self.tools.paths["zhunbei"]
                    )
                    if match_result:
                        self.tools.tap(28, 26, "找到退出按钮")
                        self.tools.tap(592, 338, "点击退出按钮")
                        self.tools.tap(408, 143, "退出")
                        break
                    self.tools.sleep(1)
                n += 1
            else:
                # 寻找准备按钮
                self.tools.find_img(
                    path=self.tools.paths["zhunbei"],
                    x=933, y=472, log="点击准备按钮")

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
        # 先从数据库获取坐标列表，如果有数据去
        n = 0
        logger.warning("数据库无数据，默认使用本地坐标")
        loc_list = self.shuffle_location()

        for loc in loc_list:
            n += 1
            self.tools.sleep(1)
            logger.info("第{}次突破".format(n))
            self.beat(loc)

            if n in (3, 6, 9):
                self.tools.sleep(1)
                self.tools.tap(167, 483)
                self.tools.sleep(1)
                self.tools.tap(167, 483)

        # 截图识别次数
        if self.tools.capture_png():
            result = self.tools.ocr_api()
            if result < 9:
                logger.warning("不足9次，停止")
                logger.info("任务完成")
            else:
                logger.success("剩余结界突破券：{}".format(result))
                self.run()
        else:
            logger.error("截图失败")


if __name__ == "__main__":
    t = TuPo()
    t.run()
