import base64
import json
import os
import random
import time
import tencentcloudKeys
import cv2
from loguru import logger
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.ocr.v20181119 import models, ocr_client


class Tools(object):
    __doc__ = "网易 MuMu 模拟器 adb 操作方法封装。"

    def __init__(self):
        self.get_devices()
        self.project_path = os.path.dirname(os.path.abspath(__file__))
        self.paths = {
            "qianshengli": os.path.join(self.project_path, "img", "qianshengli.bmp"),
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
        os.system(cmd)
        logger.debug("连接设备：{}".format(cmd))

    @staticmethod
    def sleep(n):
        """暂停 n 秒"""

        logger.debug("暂停{}秒".format(n))
        time.sleep(n)

    def tap(self, x: int, y: int, _log=None):
        """点击屏幕"""

        self.sleep(random.randint(2, 3))
        if _log:
            logger.info(_log)
        os.system(
            "adb shell input tap {} {}".format(
                random.randint(-5, 5) + x,
                random.randint(-5, 5) + y)
        )

    def swipe(self, x1: int, y1: int, x2: int, y2: int):
        """滑动屏幕"""

        self.sleep(random.randint(1, 3))
        os.system("adb shell input swipe {} {} {} {} 500".format(
            random.randint(-3, 3) + x1,
            random.randint(-3, 3) + y1,
            random.randint(-3, 3) + x2,
            random.randint(-3, 3) + y2))

    def capture_screen(self):
        """屏幕截图"""

        screen_cmd = [
            "adb shell screencap /data/screen.png",
            "adb pull /data/screen.png " + self.paths["screen"]
        ]
        for _cmd in screen_cmd:
            self.sleep(0.5)
            os.system("{} > {}".format(_cmd, self.paths['temp_file']))
        logger.debug("刷新截图文件")

    def find_img(self, path, x, y, log):
        """找图"""

        while True:
            self.capture_screen()
            match_result = self.match_img(
                capture_img=self.paths["screen"],
                temp_img=path
            )
            if match_result:
                self.tap(x, y, log)
                break
            self.sleep(2)

    @staticmethod
    def match_img(capture_img, temp_img):
        """匹配 temp_img 是否存在 capture_img 中"""

        img1 = cv2.imread(capture_img)
        img2 = cv2.imread(temp_img)
        result = cv2.matchTemplate(img1, img2, cv2.TM_CCOEFF_NORMED)
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
