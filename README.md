# 阴阳师后台全平台辅助

![screen](https://i.loli.net/2020/10/23/fMiRr75uF93t2o8.jpg)

- Python 版本：Python 3.8
- 模拟器：[雷电模拟器（推荐）](https://www.ldmnq.com/)｜[网易 MuMu](http://mumu.163.com/)  
- 模拟器分辨率：**`1024*576`**
- 网易 MuMu 显卡渲染模式：**兼容（OpenGL）**
- **兼容 Windows 系统和 MacOS 系统（不太友好，发热严重且需要重新截图）**

## 个人使用顺序

每周首先挂秘闻副本，每天三大地域鬼王，结界突破券满了挂突破，突破用完了挂御魂，大概 80-100 次左右御魂结界突破券会满，满了继续挂突破...

## 思路：

**利用 adb 截图后，使用 opencv 找图找色，模拟点击。使用 adb 操作模拟器，相当于后台操作。**

**我主要为了刷勾玉，所以此工具更侧重地域鬼王，结界突破和秘闻副本，御魂是用来刷突破券的。**

**为了防止收到鬼使黑的来信，所以增加随机等待的时间比较多，每次随机等待 2-3 秒，导致整体运行速度稍微慢了一些。**

**此工具适合放在后台干其他工作的同学使用。观赏价值不高。**

------

**地域鬼王**需要先把姑获鸟，以津真天和山童收藏。

![收藏](https://i.loli.net/2021/03/25/9VgW8nmsNKGDrtU.jpg)

**结界突破**主要是把九宫格的坐标保存到列表，使用 `shuffle` 方法随机打乱，然后循环执行。

**目前只支持个人结界突破，并且阵容需要解锁**。

![突破界面](https://i.loli.net/2021/03/25/NBIz6W1V2E5Gaxi.jpg)

第一次进入突破会主动失败一次，失败的话难度不会增加，方便刷排名和勾玉使用。

每突破三次会领取一次奖励，等待九次全部完成后，会把右上角突破剩余数量截图上传到腾讯 OCR 识别接口，如果剩余次数大于等于九次，递归执行，否则停止执行。

> 腾讯 OCR 每月有一千次免费次数。如果只是识别结界券使用，应该是够用了，如果不够用可以按需付费或者自建字典识别。

![突破剩余数量](https://i.loli.net/2020/10/23/3nSe5p8YMi9LlTw.png)

这一步需要申请 [腾讯云文字识别 OCR](https://cloud.tencent.com/product/ocr-catalog) 的 secretId 和 secretKey。

然后新建文件 `tencentcloudKeys.py`，写入：

```python

secretId = "AKI***********************aYHDtmaOw"
secretKey = "Sg**************************QdZ7X"
```

## 模拟器版

部分操作参考 [网易 MuMu 开发者必备说明书](http://mumu.163.com/help/func/20190129/30131_797867.html) 和 [【雷神命令】常用adb命令整理贴](https://www.ldmnq.com/forum/thread-32-1-1.html) 。

建议直接看雷神模拟器社区的命令整理，比较详细。

### 运行阴阳师

如果不清楚应用的启动命令，可以先手动运行该程序，然后使用命令：

```bash
adb shell dumpsys window | findstr mCurrentFocus
```

查找正在运行的应用。

启动阴阳师的命令为：

```bash
adb shell am start -n com.netease.onmyoji.netease_simulator/com.netease.onmyoji.Client
```

因为我是 iOS，只能扫码登录，所以启动命令对我来说并不实用。

### 模拟点击

例如我们需要点击 500, 266 这个坐标：

```bash
adb shell input tap 500 266
```

### 模拟滑动

从 `0, 0` 滑动到 `200, 200`，耗时 0.5 秒：

```bash
adb shell input swipe 0 0 200 200 500
```

### 截图

需要先运行此命令：

```bash
adb shell screencap /data/screen.png
```

再将截图推送到电脑：

```bash
adb pull /data/screen.png .
```

> 注意：示例中的命令将图片保存到当前路径下。

### 找图

这里借助 opencv 库实现。

```python
import cv2

def p():
    capture_img = ""  # 程序运行时的截图
    temp_img = ""  # 已经保存好的图片

    img1 = cv2.imread(capture_img)
    img2 = cv2.imread(temp_img)
    result = cv2.matchTemplate(img1, img2, cv2.TM_CCOEFF_NORMED)

    if result.max() > 0.9:
        return True
```

### 找色

如何在截图中获取某坐标的像素值？

```python
import cv2

def p(x, y):
    capture_img = ""
    _img = cv2.imread(capture_img)
    img = cv2.cvtColor(_img, cv2.COLOR_BGR2RGB)
    r, g, b = img[y, x]  # 注意这里的坐标是相反的
    return r, g, b
```

### 裁剪图片

我们截图完成以后，如何从截图中获取剩余结界突破数量？

```python
import cv2

capture_img = ""
img = cv2.imread(capture_img)
cv2.imwrite("new.png", img[12:30, 705:750])  # 裁剪坐标为 [y0:y1, x0:x1]
```

需要注意的是坐标都是 y, x。

### 双开应用切换

> 由于多开改版后（2.2.2x86/x64 版本之后）所有的多开应用和原应用都是同一个包名，所以需要通过 UserId 来控制多开的应用。

这里以**网易云游戏**为例，多开后分别获取包名，使用命令：

```bash
adb shell dumpsys window | findstr mCurrentFocus
```

全部都是 `com.netease.android.cloudgame/com.netease.android.cloudgame.MainActivity`。

所以需要通过切换 UserId 来切换应用。

通过包名来获取对应 UserId：

```bash
adb shell ps|findstr com.netease.android.cloudgame
```

返回如下内容：

![对应用户ID](https://i.loli.net/2020/10/24/Bv3CjegrU1i7XsR.png)

> 可以看到原端应用的进程 id 是 u0_a36 ，看 `_` 前面的 u0 就行，即 UserId=0;
> 在 MuMu 上一般原端的 UserId=0，多开端 #N1 的 UserId=10，如此类推 #N2 的 UserId=11，#N3 的 UserId=12，#N4 的 UserId=13

所以多开操作分为两步：

1. 切换 UserId
2. 打开应用

根据上边的截图，UserId 分别是 0 和 10，如果要在两个应用之间切换可以使用：

```bash
# 切换原应用
adb shell am start-user 0
adb shell am start --user 0 com.netease.android.cloudgame/com.netease.android.cloudgame.MainActivity

# 切换多开应用
adb shell am start-user 10
adb shell am start --user 10 com.netease.android.cloudgame/com.netease.android.cloudgame.MainActivity
```

切换之后就可以继续操作了。

### 赞赏

<div align=center><img width="260" height="260" src="https://i.loli.net/2021/01/12/ykHU2RSXoCZFfxr.jpg"></div>
