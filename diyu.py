"""
@Author: Jianxun
@Email: i@lijianxun.top
@File Name: diyu.py
@Description: 地域鬼王

"""

from loguru import logger

from tools import Tools


class DiYu(object):
    __doc__ = "每日地域鬼王，默认使用热门"

    # TODO 重写鬼王代码,尽量每一步都有图片识别，并且能识别场景

    def __init__(self):
        self.tools = Tools()

        # 右上角 筛选
        self.shaixuan = (906, 37)

        # 热门
        self.shoucang = (969, 363)

        # 姑获鸟 （选择第一个）
        self.guhuoniao = (812, 208)

        # 以津真天 （选择第二个）
        self.yijin = (807, 312)

        # 山童 （选择第三个）
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

        search_num = 0

        # 寻找进攻按钮的次数，当前设定 3，
        search_total = 3

        while True:
            self.tools.capture_screen()
            # 点击进攻按钮
            match_result = self.tools.match_img(
                capture_img=self.tools.paths["screen"],
                temp_img=self.tools.paths["tiaozhan"]
            )
            if match_result:
                self.tools.tap(925, 88, "退出\n{} - 结束".format(name))
                break

            if search_num == search_total:
                logger.warning("匹配超时，自动跳过当前操作")
                break

            search_num += 1
            logger.debug(f"第{search_num}次匹配图像")
            self.tools.sleep(1)

        self.tools.sleep(4)

    def beat(self):
        # 如果点地域鬼王出现新挑战鬼王，自动关闭
        self.tools.capture_screen()
        _color = self.tools.get_pixel(46, 47)
        logger.debug(f"像素：{_color}")
        if _color == (140, 144, 159):
            self.tools.tap(self.shaixuan[0], self.shaixuan[1])

        self.tools.tap(self.shaixuan[0], self.shaixuan[1], "点击【筛选】")

        self.tools.tap(self.shoucang[0], self.shoucang[1], "点击【热门】")

        self.tools.tap(self.guhuoniao[0], self.guhuoniao[1], "点击【鬼王】")

        self.difficulty_adjustment()

        self.tools.tap(self.tiaozhan[0], self.tiaozhan[1], "点击挑战")

        self.process("鬼王")

        # ------------------------------------------------ #

        self.tools.tap(self.shaixuan[0], self.shaixuan[1], "点击【筛选】")

        self.tools.tap(self.shoucang[0], self.shoucang[1], "点击【热门】")

        self.tools.tap(self.yijin[0], self.yijin[1], "点击【鬼王】")

        self.tools.tap(self.tiaozhan[0], self.tiaozhan[1], "点击挑战")

        self.process("鬼王")

        # ------------------------------------------------ #

        self.tools.tap(self.shaixuan[0], self.shaixuan[1], "点击【筛选】")

        self.tools.tap(self.shoucang[0], self.shoucang[1], "点击【热门】")

        self.tools.tap(self.shantong[0], self.shantong[1], "点击【鬼王】")

        self.tools.tap(self.tiaozhan[0], self.tiaozhan[1], "点击挑战")

        self.process("鬼王")


if __name__ == '__main__':
    d = DiYu()
    d.beat()
