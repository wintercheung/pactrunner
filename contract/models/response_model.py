#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2023/4/16 17:52
# @Author  : wen
# @File    : response_model.py
# @Software: PyCharm

from fastapi import Response


class VerifyPactResponse(Response):
    """
    远程验证契约返回body
    """
    verify_pact_response_success = {
        "code": 10000,
        "data": [],
        "msg": "verify pact success."
    }

    verify_pact_response_fail = {
        "code": 99999,
        "data": [],
        "msg": "Verify pact fail! Consumer name or provider name is not found in eureka, "
               "please check consumer name and provider name in eureka."
    }

    verify_pact_response_none = {
        "code": 10001,
        "data": [],
        "msg": "There is no pact need to verify."
    }


class PublishPactResponse(Response):
    """
    # 上传契约返回body
    """
    publish_pact_response_success = {
        "code": 10000,
        "data": [],
        "msg": "publish pact success."
    }

    publish_pact_response_fail = {
        "code": 99999,
        "data": [],
        "msg": "publish pact fail."
    }
