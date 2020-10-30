### 验证码机器识别--简单字符类型处理 

##### 依赖项以及使用

###### 依赖 
1. pip install openvc-python 
2. pip install pillow 
3. pip install pytesseract 
- linux 环境中 tesseract 工具
> apt install tesseract-ocr 

##### 使用:
图片处理 降噪 识别等
> import Fbil.imgToStrProcess
 
###### 暂时定为一个具有较高扩展性的python包 各个部分分离 主要有以下几个部分:
    图片文件管理分离于图像处理
*几个常用图像处理部分如:
> 基本识别 应用于无干扰图片

> 点降噪图像 

> 线降噪图像

**python文件中有详细注释**
