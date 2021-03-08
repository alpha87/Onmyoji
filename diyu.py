"""
@Author: Jianxun
@Email: i@lijianxun.top
@File Name: diyu.py
@Description: 地域鬼王

"""

from loguru import logger

from tools import Tools


class DiYu(object):
    __doc__ = "每日地域鬼王，默认姑获鸟，山童，以津真天。" \
              "需要先收藏姑获鸟，山童，以津真天。"

    def __init__(self):
        self.tools = Tools()

        # 右上角 筛选
        self.shaixuan = (906, 37)

        # 收藏
        self.shoucang = (969, 459)

        # 姑获鸟
        self.guhuoniao = (812, 208)

        # 以津真天
        self.yijin = (807, 312)

        # 山童
        self.shantong = (822, 417)

        # 挑战
        self.tiaozhan = (907, 424)

        # 40级按钮坐标
        self.jibie_40 = (327, 236)

        # 1级按钮坐标
        self.jibie_1 = (102, 241)

    def difficulty_adjustment(self):
        """难度从 40 级调整到 1 级"""

        logger.info("难度从 40 级下调至 1 级")
        self.tools.swipe(
            self.jibie_40[0],
            self.jibie_40[1],
            self.jibie_1[0],
            self.jibie_1[1]
        )

    def process(self, name):
        # 寻找准备按钮
        self.tools.find_img(
            path=self.tools.paths["zhunbei"],
            x=933, y=472, log="点击准备按钮")

        # 寻找胜利（经验页面）按钮
        self.tools.find_img(
            path=self.tools.paths["qianshengli"],
            x=416, y=83, log="点击胜利按钮")

        # 寻找胜利图标
        self.tools.find_img(
            path=self.tools.paths["shengli"],
            x=700, y=400, log="胜利")

        self.tools.tap(925, 88, "退出\n{} - 结束".format(name))
        self.tools.sleep(2)

    def beat(self):
        # ------------------------------------------------ #

        # 姑获鸟

        self.tools.tap(self.shaixuan[0], self.shaixuan[1], "点击【筛选】")

        self.tools.tap(self.shoucang[0], self.shoucang[1], "点击【收藏】")

        self.tools.tap(self.guhuoniao[0], self.guhuoniao[1], "点击【姑获鸟】")

        self.difficulty_adjustment()

        self.tools.tap(self.tiaozhan[0], self.tiaozhan[1], "点击挑战")

        self.process("姑获鸟")

        # ------------------------------------------------ #

        # 以津真天

        self.tools.tap(self.shaixuan[0], self.shaixuan[1], "点击【筛选】")

        self.tools.tap(self.shoucang[0], self.shoucang[1], "点击【收藏】")

        self.tools.tap(self.yijin[0], self.yijin[1], "点击【以津真天】")

        self.tools.tap(self.tiaozhan[0], self.tiaozhan[1], "点击挑战")

        self.process("以津真天")

        # ------------------------------------------------ #

        # 山童

        self.tools.tap(self.shaixuan[0], self.shaixuan[1], "点击【筛选】")

        self.tools.tap(self.shoucang[0], self.shoucang[1], "点击【收藏】")

        self.tools.tap(self.shantong[0], self.shantong[1], "点击【山童】")

        self.tools.tap(self.tiaozhan[0], self.tiaozhan[1], "点击挑战")

        self.process("山童")


if __name__ == '__main__':
    d = DiYu()
    d.beat()
