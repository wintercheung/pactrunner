#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2023/4/16 17:51
# @Author  : wen
# @File    : request_model.py
# @Software: PyCharm

from typing import List, Dict
from pydantic import BaseModel


class VerifyPactModel(BaseModel):
    """
    远程执行契约返回模型
    """
    pacts: List[Dict]