#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2023/4/16 18:10
# @Author  : wen
# @File    : run.py
# @Software: PyCharm

import uvicorn

uvicorn.run("api.main:app", host="127.0.0.1", port=8000)
