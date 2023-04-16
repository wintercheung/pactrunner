#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2023/4/16 17:39
# @Author  : wen
# @File    : __init__.py.py
# @Software: PyCharm

from fastapi import FastAPI
from contract.config.logger import logger
from contract.routes import router


def create_app():
    app = FastAPI()
    logger.info("注册路由")
    app.include_router(router.router, prefix="")
    return app
