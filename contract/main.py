#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2023/4/16 18:09
# @Author  : wen
# @File    : main.py
# @Software: PyCharm

import asyncio

from contract import create_app
from concurrent.futures.process import ProcessPoolExecutor

app = create_app()


# 多线程
async def run_in_process(fn, *args):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(app.state.executor, fn, *args)  # wait and return result


# 开启线程池
@app.on_event("startup")
async def on_startup():
    app.state.executor = ProcessPoolExecutor()


# 关闭线程池
@app.on_event("shutdown")
async def on_shutdown():
    app.state.executor.shutdown()
