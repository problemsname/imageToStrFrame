#!/usr/bin/env python
# coding=utf-8

import os
import cv2
from PIL import Image 
from pytesseract import *


#基于内聚性与耦合性
#若将路径设置区分开则工作量过大
#若在一个类中则不利于以后扩展
#所以使用继承以及字类扩充



class imgToStrProcess:
    '''
        图片处理类功能有限只对简单字符型验证码可以识别且有准确性
        可以作为测试或者机器学习提供训练集
        基础的二值化转灰度 是必须使用
        如果验证码非常简单可以直接进行识别

        去除边框处理存在边框的验证码

        降噪分为点降噪,线降噪
        分别处理 点干扰较多验证码图片类型
                线干扰较多验证码图片类型
        图片识别显示
        图片识别保存

        备注：
            1. 添加字符粘连类型验证码图片
            2. 子类扩展 提供多线程处理 机器学习框架搭建
            3. 渗透工具使用
            4. 爬虫工具使用
            5. 目录操作部分冗余性较高 可以在模块调用之前判断
    '''

    def __int__(self,imgName):
        # 图片保存路径
        #此处为默认值若需要另外设置需要使用字类调用函数进行设置
        self.imageFilesPath = "./rawImgs/"  # 原始图片位置
        self.binaryPath = "./imgbinary/"  # 转灰度 与二值化
        self.clearFramepath = "./imCFrame/"  # 去除边框
        self.pointProcessPath = "./IPoint/"  # 点降噪
        self.lineProcessPath = "./ILine/"  # 线降噪

    def fileJudge(self,fileNameorPath):
        if not os.path.exists(fileNameorPath):
            print("error:%s file does not exist!"%fileNameorPath)
            exit(2)
            #此处应该修改目录没有找到则应该创建

    #图片灰度和二值化
    def binary_image(self,img_name):
        print("--------Binary and Grayscale start")
        imageFile=self.imageFilesPath+img_name
        self.fileJudge(imageFile)
        print("....loading: "+imageFile)
        img = cv2.imread(imageFile)
        #图片读取加载

        img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        #图片灰度化

        binaryimage = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,21,1)
        #二值化

        print("process done"+img_name)
        if not os.path.exists(self.binaryPath):
            os.mkdir(self.binaryPath)
        cv2.imwrite(self.binaryPath+img_name,binaryimage)
        #处理后的图片保存
        print("save image file to %s"%self.binaryPath+img_name)
        #图片返回等待下个函数处理
        return binaryimage

    #去除边框如果有边框的话
    def  clearframe(self,img_name,width=1):
        #img 需要清理边框的图片 width 宽的宽度
        print("--------Clear frame start")
        imageFile = self.binaryPath+img_name
        self.fileJudge(imageFile)
        print("....loading: "+imageFile)

        img = cv2.imread(imageFile)
        h,w=img.shape[:2]
        for y in range(0,w):
            for x in range(0,h):
                if y < 2 or y > w - 2:
                    img[x,y]=255
                if x < 2 or x > h - 2:
                    img[x,y]=255

        print("process done"+img_name)
        if not os.path.exists(self.clearFramepath):
            os.mkdir(self.clearFramepath)
        cv2.imwrite(self.clearFramepath+img_name)
        print("save image file to %s"%self.clearFramepath+img_name)
        return img

    #图片降噪---------干扰线降噪 可以尝试多次降噪
    def interference_line(self,img_name):
        '''
        线降噪 判断某点四个方向：上下左右 是否存在连接如果大于两个则为字符
        :param img_name:
        :return:
        '''
        print("--------Line noise reduction start")
        imageFile = self.clearFramepath+img_name
        self.fileJudge(imageFile)
        print("....loading: "+imageFile)
        img = cv2.imread(imageFile)

        h,w=img.shape[:2]
        #opencv矩阵点是反的
        #img[1,2] 1:图片的高度2:图片的宽度
        for y in range(1,w - 1):
            for x in range(1,h - 1):
                count=0
                if img[x , y - 1] > 245:#y 表示左右 x 表示上下
                    count += 1
                if img[x , y + 1] > 245:
                    count += 1
                if img[x - 1 , y] > 245:
                    count += 1
                if img[x + 1 , y] > 245:
                    count += 1
                if count > 2:
                    img[x , y] = 255 #如果附近四个方向有两个是有颜色的则是字符
        print("process done" + img_name)
        if not os.path.exists(self.lineProcessPath):
            os.mkdir(self.lineProcessPath)
        cv2.imwrite(self.lineProcessPath+img_name)
        print("save image file to %s"%self.lineProcessPath+img_name)
        return img

    #降噪 -----------点降噪
    def interference_point(self,img_name,x = 0,y = 0):
        """
        判断某点是否为孤立的点
            点是否为字符判断范围大于线降噪
            周围田字框
        """
        print("--------Point noise reduction start")
        imageFile = self.lineProcessPath+img_name
        self.fileJudge(imageFile)
        print("....loading: " + imageFile)
        img = cv2.imread(imageFile)

        cur_pixel = img[x,y]#当前像素点的值
        height,width = img.shape[:2]

        for y in range(0, width - 1):
          for x in range(0, height - 1):
            if y == 0:  # 第一行
                if x == 0:  # 左上顶点,4邻域
                    # 中心点旁边3个点
                    sum = int(cur_pixel) \
                          + int(img[x, y + 1]) \
                          + int(img[x + 1, y]) \
                          + int(img[x + 1, y + 1])
                    if sum <= 2 * 245:
                      img[x, y] = 0
                elif x == height - 1:  # 右上顶点
                    sum = int(cur_pixel) \
                          + int(img[x, y + 1]) \
                          + int(img[x - 1, y]) \
                          + int(img[x - 1, y + 1])
                    if sum <= 2 * 245:
                      img[x, y] = 0
                else:  # 最上非顶点,6邻域
                    sum = int(img[x - 1, y]) \
                          + int(img[x - 1, y + 1]) \
                          + int(cur_pixel) \
                          + int(img[x, y + 1]) \
                          + int(img[x + 1, y]) \
                          + int(img[x + 1, y + 1])
                    if sum <= 3 * 245:
                      img[x, y] = 0
            elif y == width - 1:  # 最下面一行
                if x == 0:  # 左下顶点
                    # 中心点旁边3个点
                    sum = int(cur_pixel) \
                          + int(img[x + 1, y]) \
                          + int(img[x + 1, y - 1]) \
                          + int(img[x, y - 1])
                    if sum <= 2 * 245:
                      img[x, y] = 0
                elif x == height - 1:  # 右下顶点
                    sum = int(cur_pixel) \
                          + int(img[x, y - 1]) \
                          + int(img[x - 1, y]) \
                          + int(img[x - 1, y - 1])

                    if sum <= 2 * 245:
                      img[x, y] = 0
                else:  # 最下非顶点,6邻域
                    sum = int(cur_pixel) \
                          + int(img[x - 1, y]) \
                          + int(img[x + 1, y]) \
                          + int(img[x, y - 1]) \
                          + int(img[x - 1, y - 1]) \
                          + int(img[x + 1, y - 1])
                    if sum <= 3 * 245:
                      img[x, y] = 0
            else:  # y不在边界
                if x == 0:  # 左边非顶点
                    sum = int(img[x, y - 1]) \
                          + int(cur_pixel) \
                          + int(img[x, y + 1]) \
                          + int(img[x + 1, y - 1]) \
                          + int(img[x + 1, y]) \
                          + int(img[x + 1, y + 1])

                    if sum <= 3 * 245:
                      img[x, y] = 0
                elif x == height - 1:  # 右边非顶点
                    sum = int(img[x, y - 1]) \
                          + int(cur_pixel) \
                          + int(img[x, y + 1]) \
                          + int(img[x - 1, y - 1]) \
                          + int(img[x - 1, y]) \
                          + int(img[x - 1, y + 1])

                    if sum <= 3 * 245:
                      img[x, y] = 0
                else:  # 具备9领域条件的
                    sum = int(img[x - 1, y - 1]) \
                          + int(img[x - 1, y]) \
                          + int(img[x - 1, y + 1]) \
                          + int(img[x, y - 1]) \
                          + int(cur_pixel) \
                          + int(img[x, y + 1]) \
                          + int(img[x + 1, y - 1]) \
                          + int(img[x + 1, y]) \
                          + int(img[x + 1, y + 1])
                    if sum <= 4 * 245:
                      img[x, y] = 0
        print("process done" + img_name)
        if not os.path.exists(self.pointProcessPath):
            os.mkdir(self.pointProcessPath)
        cv2.imwrite(self.pointProcessPath+img_name)
        print("save image file to %s"%self.pointProcessPath+img_name)
        return img

    def imageDistoShow(self,imageFile):
        #识别并显示图片
        #
        self.fileJudge(imageFile)
        print("starting extract image%s"%imageFile)
        print("....loading: " + imageFile)

        img = Image.open(imageFile)
        try:
            imgString = image_to_string(img)
        except Exception as err:
            print("error: image_to_string %s"%imageFile)
            exit(2)

        print("The verification code is: "+imgString)
        img.show()
        return imgString

    def imageDistoSave(self,imageFile):
        #识别并保存到文件
        #
        self.fileJudge(imageFile)
        codeFile=open("./code.txt",'a+')
        img = Image.open(imageFile)

        try:
            imgString = image_to_string(img)
        except Exception as err:
            print("error: image_to_string %s"%imageFile)
            exit(2)
        codeFile.write(imageFile+':'+imgString+'\n')
        codeFile.close()

        return imgString