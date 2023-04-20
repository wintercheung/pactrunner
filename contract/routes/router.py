#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2023/4/16 17:54
# @Author  : wen
# @File    : router.py
# @Software: PyCharm

import ujson

from typing import List
from fastapi import APIRouter, UploadFile, File
from starlette.responses import HTMLResponse

from contract.models.request_model import VerifyPactModel
from contract.models.response_model import VerifyPactResponse, PublishPactResponse
from contract.utils.publish_pact import PublishPact
from contract.utils.verify_pact import VerifyPact


router = APIRouter()


@router.post("/contract/verify-pact", tags=["contract"])
async def verify_pact_api(pacts: VerifyPactModel):
    """
    验证契约文件接口
    :type pacts: list[dict]
    :param pacts: 消费者-生产者键值对
    :return:
    """
    vp = VerifyPact(pact_data=pacts)
    vp.verify_data()
    return VerifyPactResponse.verify_pact_response_success()


@router.post("/contract/publish-pact", tags=["contract"])
async def create_upload_files(files: List[UploadFile] = File(...)):
    """
    上传契约文件接口
    :param files: 上传的 json 文件
    :return:
    """
    try:
        for file in files:
            data = ujson.loads(await file.read())
            PublishPact(data).publish_pact()
    except Exception as e:
        return PublishPactResponse.publish_pact_response_fail, e
    return PublishPactResponse.publish_pact_response_success


@router.get("/contract/tools/publish-pact")
async def test_tools_publish_pact():
    content = """
    <body>
    <form action="/contract/publishPact/" enctype="multipart/form-data" method="post">
    <input name="files" type="file" multiple>
    <input type="submit" value="上传">
    </form>
    </body>
    """
    return HTMLResponse(content=content)
