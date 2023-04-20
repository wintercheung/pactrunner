#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2023/4/16 18:03
# @Author  : wen
# @File    : eureka_ip.py
# @Software: PyCharm

import requests
from bs4 import BeautifulSoup
from contract.config import eureka
from contract.config.logger import logger


class EurekaIp:
    def __init__(self):
        self.url = eureka.EUREKA_URL

    def request_eureka(self):
        response = requests.get(self.url).text
        logger.info("请求Eureka的地址获取页面内容: \n" + response)
        return response

    def parse_eureka(self, server_name):
        soup = BeautifulSoup(self.request_eureka(), "lxml")
        tables = [
            [
                [td.get_text(strip=True) for td in tr.find_all('td')]
                for tr in table.find_all('tr')
            ]
            for table in soup.find_all('table')
        ]
        logger.info("提取Eureka页面内容中的table属性的值: \n" + str(tables))
        logger.info("提取Eureka页面内容中的table[2]属性的值: \n" + str(tables[2]))
        server_dict = {}
        for table in tables[2]:
            if table and table[0] == server_name:
                logger.info("检查Eureka中微服务名所在的table属性值: \n" + str(table))
                logger.info("检查Eureka中的微服务名是否与需求服务匹配: \n" + str(table[0]))
                server_dict[table[0]] = table[3].split(" -")[1]

        logger.info("检查提取出的微服务ip对: \n" + str(server_dict))
        if server_dict == {}:
            msg = "The server is not found in eureka, please check server name."
            logger.error(msg)
            return msg
        for i in server_dict:
            server_ips = server_dict[i].split(",")
            for ip in server_ips:
                if eureka.ENV_CODE in ip:
                    logger.info("检查提取出来的微服务对应的ip: \n" + str(ip.split(":")[0]))
                    server_ip = ip.split(":")[0]
                    return server_ip
