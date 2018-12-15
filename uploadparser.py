#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-12-15 09:58:55
# @Author  : lixint (lixint8@gmail.com)
# @Link    : https://github.com/lixint/
# @Version : $Id$
import re
import requests
import json
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import sys
import logging
import os
import time
import shutil
from urllib import parse
from configparser import ConfigParser

class UploadImg(object):
	'''md文件图片上传'''
	__is_exist = os.path.exists
	def __init__(self,filename):
		self.__filename = filename #传入为文章文件完整路径
		with open(filename,"r",encoding="utf-8") as md:
			self.file_content = md.read()
		

	#上传腾讯云cos
	def tx_upload(self,img_origin_url):
		try:
			secret_id = self.__tx_s_id	  # 替换为用户的 secretId
			secret_key = self.__tx_s_key	  # 替换为用户的 secretKey
			region = self.__tx_region	 # 替换为用户的 Region
			Bucket = self.__tx_Bucket #替换为用户的Bucket
			token = None				# 使用临时密钥需要传入 Token，默认为空，可不填
			scheme = 'https'			# 指定使用 http/https 协议来访问 COS，默认为 https，可不填
			config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
			client = CosS3Client(config)
			img_basename = os.path.basename(img_origin_url)
			#time_for_dir = time.strftime("%Y-%m-%d")
			#获取文章文件名用于创建文件夹
			article_basename = os.path.basename(self.__filename)		#获取文章文件名及后缀
			article_name = os.path.splitext(article_basename)[0]	#splitext返回（文件名，扩展名的数组），提取文件名
			
			#上传后建立一个以当前日期命名的文件夹，如果不需要，注释掉这一行用下一行。
			#cloud_path = time_for_dir + r'/' + img_basename

			#上传后建立一个以文件名命名的文件夹，如果不需要，注释掉用下一行
			cloud_path = article_name + r'/' + img_basename

			#上传至根目录，不创建文件夹
			#cloud_path = img_basename

			key = cloud_path
			with open(img_origin_url, 'rb') as fp:
				response = client.put_object(
					Bucket=Bucket,
					Body=fp,
					Key=key,
					#StorageClass='STANDARD',
					#ContentType='text/html; 
					#charset='utf-8'
				)
			cloud_path = client._conf.uri(bucket=Bucket, path=key)
			return cloud_path
		except BaseException as err:
			print("error in tx\n{}".format(err))

	#上传smms
	def smms_upload(self,img_origin_url):
		try:
			smms_url = 'https://sm.ms/api/upload'
			data = requests.post(
				smms_url,
				files={'smfile':open(img_origin_url,'rb'),'format':'json'}
			)
			img_new_url = json.loads(data.text)
			cloud_path = img_new_url['data']['url'] 
			return(cloud_path)
		except BaseException as err:
			print("error in smms\n{}".format(err))

	#本地引用
	def local_upload(self):
		pass
	'''
	#获取文档中的![]()图片插入块
	def get_img_block(self,filename):
		img_block = re.findall(r'!\[.*?\)', self.file_content)
		return img_block
	'''
	#修改图片
	def change_img_path(self,upload_method):
		try:
			img_block = re.findall(r'!\[.*?\)', self.file_content)
			article_content = self.file_content
			if upload_method == "smms":
				for i in range(len(img_block)):
					img_origin_url = re.findall(r'\((.*?)\)',img_block[i]) #获取插入图片时图片路径
					if not UploadImg.__is_exist(img_origin_url[0]):
						continue
					img_new_url = self.smms_upload(img_origin_url[0])
					article_content = article_content.replace(img_origin_url[0],img_new_url)
					#print("at is {}\n,ft is {}\n,iou is {}\n,inu is {}".format(article_content,self.file_content,img_origin_url,img_new_url))
			elif upload_method == "tx":
				self.loadconf()
				for i in range(len(img_block)):
					img_origin_url = re.findall(r'\((.*?)\)',img_block[i]) #获取插入图片时图片路径
					if not UploadImg.__is_exist(img_origin_url[0]):
						continue
					img_new_url = self.tx_upload(img_origin_url[0])
					article_content = article_content.replace(img_origin_url[0],img_new_url)
			elif upload_method == "local":
				for i in range(len(img_block)):
					img_origin_url = re.findall(r'\((.*?)\)',img_block[i]) #获取插入图片时图片路径
					if not UploadImg.__is_exist(img_origin_url[0]):
						continue
					img_new_url = self.smms_upload(img_origin_url[0])
					article_content = article_content.replace(img_origin_url[0],img_new_url)
			else:
				print("part of change_img_path error")
			return article_content
		except BaseException as err:
			print("error in change_img_path\n{}".format(err))

	#文档写
	def md_write(self,article_content):
		try:
			with open (self.__filename,'w',encoding = 'utf-8') as md:
				md.write(article_content)
		except BaseException as err:
			print("error in md_write\n{}".format(err))

	# 腾讯cos专用，加载配置
	def loadconf(self):
		cfg = ConfigParser()
		try:
			cfg.read(r'UploadImg.ini')
			self.__tx_s_id=cfg.get('tx','secret_id')
			self.__tx_s_key=cfg.get('tx','secret_key')
			self.__tx_region=cfg.get('tx','region')
			self.__tx_Bucket=cfg.get('tx','Bucket')
		except BaseException as err:
			print("error in loadconf\n{},please check your config file".format(err))

	#去除空行
	def clearblankline(self,article_content):
		try:
			content_split = article_content.splitlines(True) #str => list
			while "\n" in content_split:
				content_split.remove("\n")
			final_content = "".join(content_split)
			return final_content
		except BaseException as err:
			print("error in clearblankline\n{},please check your config file".format(err))


if __name__ == '__main__':
	foo = UploadImg(r"D:\Github\1.md")
	#foo.loadconf()
	at = foo.change_img_path("smms")
	at2 = foo.clearblankline(at)
	foo.md_write(at2)
	print(at2)
