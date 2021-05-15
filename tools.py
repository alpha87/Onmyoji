"""
@Author: Jianxun
@Email: i@lijianxun.top
@File Name: tools.py
@Description: 包含网易 MuMu 模拟器 adb 操作，腾讯云文字识别。

"""

import base64
import json
import os
import random
import time
from subprocess import PIPE, run

import cv2
from loguru import logger
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.ocr.v20181119 import models, ocr_client

import tencentcloudKeys


class Tools(object):
    __doc__ = "网易 MuMu 模拟器 adb 操作方法封装。"

    def __init__(self):
        self.get_devices()
        self.project_path = os.path.dirname(os.path.abspath(__file__))
        self.flag = False
        self.paths = {
            "qianshengli": os.path.join(self.project_path, "img", "qianshengli.bmp"),
            "jingong": os.path.join(self.project_path, "img", "jingong.bmp"),
            "tiaozhan": os.path.join(self.project_path, "img", "tiaozhan.bmp"),
            "shengli": os.path.join(self.project_path, "img", "shengli.bmp"),
            "zhunbei": os.path.join(self.project_path, "img", "zhunbei.bmp"),
            "screen": os.path.join(self.project_path, "img", "screen.png"),
            "num": os.path.join(self.project_path, "img", "num.png"),
            "screen_files": os.path.join(self.project_path, "img"),
            "temp_file": os.path.join(self.project_path, "temp.txt")
        }

    @staticmethod
    def get_devices():
        """连接设备"""

        cmd = "adb connect 127.0.0.1:7555"
        run(cmd, universal_newlines=True, shell=True)
        logger.debug("连接设备")

    @staticmethod
    def sleep(n=0.0):
        """暂停 n 秒"""

        if not n:
            n = random.randint(1, 3)
        logger.debug("暂停{}秒".format(n))
        time.sleep(n)

    @staticmethod
    def launch_onmyoji():
        run("adb shell am start -n com.netease.onmyoji.netease_simulator/com.netease.onmyoji.Client")
        logger.debug("启动阴阳师")

    def tap(self, x: int, y: int, _log=None):
        """点击屏幕"""

        if _log:
            logger.info(_log)
        run("adb shell input tap {} {}".format(
            random.randint(-5, 5) + x,
            random.randint(-5, 5) + y),
            universal_newlines=True,
            shell=True)
        self.sleep(random.randint(2, 4))

    def swipe(self, x1: int, y1: int, x2: int, y2: int):
        """滑动屏幕"""

        self.sleep()
        run("adb shell input swipe {} {} {} {} 500".format(
            random.randint(-3, 3) + x1,
            random.randint(-3, 3) + y1,
            random.randint(-3, 3) + x2,
            random.randint(-3, 3) + y2),
            universal_newlines=True,
            shell=True)
        self.sleep()

    def capture_screen(self):
        """屏幕截图"""

        screen_cmd = [
            "adb shell screencap /data/screen.png",
            "adb pull /data/screen.png " + self.paths["screen"],
            "adb shell rm /data/screen.png"
        ]
        self.sleep(0.5)
        for _cmd in screen_cmd:
            self.sleep(n=0.1)
            run(_cmd, stdout=PIPE, stderr=PIPE,
                universal_newlines=True, shell=True)
        self.sleep(0.5)
        logger.debug("刷新截图文件")

    def find_img(self, path, x, y, log, thread_flag=False):
        """找图"""

        while True:
            if self.flag and thread_flag:
                logger.debug("已经匹配到其中一张图，退出...")
                self.flag = False
                self.sleep(0.5)
                break

            self.capture_screen()
            match_result = self.match_img(
                capture_img=self.paths["screen"],
                temp_img=path
            )
            if match_result:
                if thread_flag:
                    self.flag = True
                self.tap(x, y, log)
                break
            self.sleep(0.5)

    @staticmethod
    def match_img(capture_img, temp_img):
        """匹配 temp_img 是否存在 capture_img 中"""

        img1 = cv2.imread(capture_img)
        img2 = cv2.imread(temp_img)
        result = cv2.matchTemplate(img1, img2, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        logger.debug("截图对比:\n{}\n{}\n{}\n{}".format(min_val, max_val, min_loc, max_loc))
        if result.max() > 0.9:
            return True
        return False

    def get_pixel(self, x, y):
        """获取截图中坐标对应像素值"""

        _img = cv2.imread(self.paths["screen"])
        img = cv2.cvtColor(_img, cv2.COLOR_BGR2RGB)
        r, g, b = img[y, x]  # 注意这里的坐标是相反的
        return r, g, b

    def capture_png(self):
        """裁剪结界券"""

        self.capture_screen()
        img = cv2.imread(self.paths["screen"])
        # 裁剪坐标为 [y0:y1, x0:x1]
        cv2.imwrite(self.paths["num"], img[10:40, 829:892])
        logger.debug("结界券数量图片裁剪完成")
        return True

    def ocr_api(self):
        with open(self.paths["num"], "rb") as f:
            # 转为二进制格式
            base64_data = base64.b64encode(f.read())

        cred = credential.Credential(tencentcloudKeys.secretId,
                                     tencentcloudKeys.secretKey)
        httpProfile = HttpProfile()
        httpProfile.endpoint = "ocr.tencentcloudapi.com"
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = ocr_client.OcrClient(cred, "ap-beijing", clientProfile)
        req = models.GeneralBasicOCRRequest()
        params = {"ImageBase64": str(base64_data, encoding="utf-8"), }
        req.from_json_string(json.dumps(params))
        resp = client.GeneralBasicOCR(req)
        result = json.loads(resp.to_json_string())

        # 识别出的文字，已经是最终剩余数量 < >/30
        result_text = result["TextDetections"][0]["DetectedText"]
        result_text = int(result_text.split("/")[0].replace(" ", ""))
        return result_text
