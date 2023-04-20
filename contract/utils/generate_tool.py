#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2023/4/16 18:00
# @Author  : wen
# @File    : generate_tool.py
# @Software: PyCharm

from datetime import datetime
from contract.config.logger import logger


def generate_version():
    """
    根据当前时间生成时间版本
    :return: 时间版本号
    """
    now = datetime.now()
    version = now.strftime("%Y_%m_%d-%H_%M_%S")
    logger.info("生成的版本号为: \n" + str(version))
    return version
