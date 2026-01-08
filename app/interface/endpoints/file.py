#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2025/12/12 21:06
@Author : YangFei
@File   : file.py
@Desc   : 文件模块路由
"""
from fastapi import APIRouter, Depends

from app.interface.schemas.base import Response
from app.interface.schemas.file import FileReadRequest, FileWriteRequest
from app.interface.service_dependencies import get_file_service
from app.models.file import FileReadResult, FileWriteResult
from app.services.file import FileService

# 文件模块路由
router = APIRouter(prefix='/files', tags=['文件模块'])


@router.post(
    path='/read-file',
    response_model=Response[FileReadResult]
)
async def read_file(
        request: FileReadRequest,
        file_service: FileService = Depends(get_file_service)
) -> Response[FileReadResult]:
    """ 读取文件 """
    # 调用文件服务读取文件内容
    result = await file_service.read_file(
        file_path=request.file_path,
        start_line=request.start_line,
        end_line=request.end_line,
        sudo=request.sudo,
        max_length=request.max_length,
    )

    return Response.success(msg='文件内容读取成功', data=result)


@router.post(
    path='/write-file',
    response_model=Response[FileWriteResult]
)
async def write_file(
        request: FileWriteRequest,
        file_service: FileService = Depends(get_file_service)
) -> Response[FileWriteResult]:
    """ 写入文件 """
    # 调用文件服务写入文件内容
    result = await file_service.write_file(
        file_path=request.file_path,
        content=request.content,
        append=request.append,
        leading_newline=request.leading_newline,
        trailing_newline=request.trailing_newline,
        sudo=request.sudo,
    )

    return Response.success(msg='文件内容写入成功', data=result)
