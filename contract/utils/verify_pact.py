#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2023/4/16 18:00
# @Author  : wen
# @File    : verify_pact.py
# @Software: PyCharm

import subprocess

from contract.config import broker
from contract.config.logger import logger
from contract.utils.eureka_ip import EurekaIp
from contract.utils.generate_tool import generate_version


class VerifyPact:
    def __init__(self, pact_data):
        self.base_url = broker.PACT_BROKER_BASE_URL
        self.pact_data = pact_data

    def verify_pact(self, consumer, provider):
        """
        推送到pact broker并且远程执行pact文件验证契约
        :return: 参数列表
        """
        version = generate_version()
        provider_part = "provider/" + provider
        consumer_part = "/consumer/" + consumer

        # 远程验证契约文件
        EI = EurekaIp()
        provider_ip = EI.parse_eureka(provider)
        logger.info("远程验证生产者服务ip: \n" + provider_ip)
        # 拼接生产者的 url
        provider_base_url = "http://" + provider_ip + ":8080"
        pact_urls = self.base_url + "pacts/" + provider_part + consumer_part + "/latest"
        logger.info("远程验证的pact json的地址是: \n" + pact_urls)
        verifier_command = subprocess.Popen([
            "pact-verifier",
            "--provider-base-url=" + provider_base_url,
            "--pact-urls=" + pact_urls,
            "-r",
            "-a",
            version
        ])
        verifier_command.wait(timeout=10)
        verifier_return_code = verifier_command.returncode
        logger.info("命令返回值为: " + str(verifier_return_code))
        if verifier_return_code == 0:
            msg_case_success = "All the testcases were successfully executed"
            logger.info("远程验证命令执行结果: \n" + msg_case_success)
            return msg_case_success
        elif verifier_return_code == 1:
            msg_case_fail = "The testcases error or pacts error"
            logger.warning("远程验证命令执行结果: \n" + msg_case_fail)
            return msg_case_fail
        else:
            msg = "The command is error!"
            logger.error("远程验证命令执行结果: \n" + msg)
            return msg

    def verify_data(self):
        pacts_dict = dict(self.pact_data)["pacts"]
        logger.info("接收执行契约对参数: \n" + str(pacts_dict))
        for items in pacts_dict:
            for key, value in items.items():
                logger.info(key + ":" + value)
                consumer = value
                provider = key
                logger.info(consumer + ": " + provider)
                try:
                    self.verify_pact(provider, consumer)
                except:
                    pass
