#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2023/4/16 17:56
# @Author  : wen
# @File    : publish_pact.py
# @Software: PyCharm


import requests
import ujson

from contract.config import broker
from contract.utils.generate_tool import generate_version
from contract.config.logger import logger


class PublishPact:
    def __init__(self, data):
        self.consumer = None
        self.provider = None
        self.data = data
        logger.info("json解析上传broker的数据是: \n" + str(data))
        self.headers = {"Content-Type": "application/json;charset=UTF-8"}

    def json_parser(self):
        """
        解析pact json文件提取有效字段
        :return: 返回生产者和消费者
        """
        self.consumer = self.data["consumer"]["name"]
        logger.info("json解析提取到的消费者名称是: \n" + str(self.consumer))
        self.provider = self.data["provider"]["name"]
        logger.info("json解析提取到的生产者名称是: \n" + str(self.provider))
        return self.provider, self.consumer

    def publish_limited(self, server_name):
        """
        首次发布放开发布限制
        :return:
        """
        body_data = {"name": server_name}
        response = requests.post(
            url=broker.PACT_BROKER_BASE_URL + '/pacticipants',
            headers=self.headers,
            json=body_data)

        if response.status_code == 201:
            return True
        else:
            logger.info("首次上传解开限制新建pacticipants: \n" + str(response.text))
            logger.error("首次上传解开限制失败: \n" + str(response.status_code))
            return response.text

    def publish_pact(self):
        """
        推送到pact broker并且远程执行pact文件验证契约
        :return: 参数列表
        """
        provider_part = "provider/" + self.json_parser()[0]
        consumer_part = "/consumer/" + self.json_parser()[1]
        version_part = "/version/" + generate_version()

        # 推送pact文件
        pact_request_url = broker.PACT_BROKER_BASE_URL + "pacts/" + provider_part + consumer_part + version_part
        logger.info("上传地址为: \n" + pact_request_url)
        response = requests.put(url=pact_request_url, headers=self.headers, data=ujson.dumps(self.data))
        logger.info("上传结果为: \n" + str(response.text))
        if response.status_code == 201:
            return True
        elif response.status_code == 409:
            self.publish_limited(server_name=self.consumer)
            self.publish_limited(server_name=self.provider)
            response = requests.put(url=pact_request_url, headers=self.headers, data=ujson.dumps(self.data))
            logger.info("上传结果为: \n" + str(response.text))
            return response.status_code, response.text
        else:
            logger.info("上传结果为: \n" + str(response.text))
            return response.status_code, response.text
