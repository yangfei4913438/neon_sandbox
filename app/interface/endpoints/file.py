#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2025/12/12 21:06
@Author : YangFei
@File   : file.py
@Desc   : 文件模块路由
"""
import os
from fastapi import APIRouter, Depends, File, Form, UploadFile
from fastapi.responses import FileResponse

from app.interface.schemas.base import Response
from app.interface.schemas.file import FileReadRequest, FileWriteRequest, FileReplaceRequest, FileSearchRequest, \
    FileFindRequest, FileCheckRequest, FileDeleteRequest
from app.interface.service_dependencies import get_file_service
from app.models.file import FileReadResult, FileWriteResult, FileReplaceResult, FileSearchResult, FileFindResult, \
    FileUploadResult, FileCheckResult, FileDeleteResult
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


@router.post(
    path="/replace-in-file",
    response_model=Response[FileReplaceResult],
)
async def replace_in_file(
        request: FileReplaceRequest,
        file_service: FileService = Depends(get_file_service),
) -> Response[FileReplaceResult]:
    """根据传递的数据替换文件内的部分内容"""
    result = await file_service.replace_in_file(
        file_path=request.file_path,
        old_str=request.old_str,
        new_str=request.new_str,
        sudo=request.sudo,
    )

    return Response.success(
        msg=f"文件内容替换完成, 已替换{result.replaced_count}处内容",
        data=result,
    )


@router.post(
    path="/search-in-file",
    response_model=Response[FileSearchResult],
)
async def search_in_file(
        request: FileSearchRequest,
        file_service: FileService = Depends(get_file_service),
) -> Response[FileSearchResult]:
    """根据传递的数据检索指定文件的内容"""
    result = await file_service.search_in_file(
        file_path=request.file_path,
        regex=request.regex,
        sudo=request.sudo,
    )

    return Response.success(
        msg=f"文件内容搜索完成, 找到{len(result.matches)}处匹配内容",
        data=result,
    )


@router.post(
    path="/find-files",
    response_model=Response[FileFindResult],
)
async def find_files(
        request: FileFindRequest,
        file_service: FileService = Depends(get_file_service),
) -> Response[FileFindResult]:
    """根据传递的文件夹+glob文件规则查找文件列表"""
    result = await file_service.find_files(
        dir_path=request.dir_path,
        glob_pattern=request.glob_pattern,
    )

    return Response.success(
        msg=f"查找完毕, 检索到{len(result.files)}个文件",
        data=result,
    )


@router.post(
    path="/upload-file",
    response_model=Response[FileUploadResult],
)
async def upload_file(
        file: UploadFile = File(...),  # 上传的文件源，接收文件
        file_path: str = Form(None),  # 上传的文件路径, 表单传递
        file_service: FileService = Depends(get_file_service),
) -> Response[FileUploadResult]:
    """根据传递的文件源+路径上传文件到沙箱"""
    # 1.判断filepath是否传递，如果没有则使用临时路径
    if not file_path:
        file_path = f"/tmp/{file.filename}"

    # 2.调用服务将文件上传至沙箱
    result = await file_service.upload_file(file=file, file_path=file_path)

    return Response.success(
        msg="文件上传成功",
        data=result,
    )


@router.get(path="/download-file")
async def download_file(
        file_path: str,
        file_service: FileService = Depends(get_file_service),
) -> FileResponse:
    """根据传递的filepath下载指定的文件"""
    # 1.确保下当前文件存在
    await file_service.ensure_file(file_path)

    # 2.提取文件名字
    filename = os.path.basename(file_path)

    # 3.返回文件下载响应
    # http://127.0.0.1:6001/api/file/download-file?file_path=./files/wuye.md
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/octet-stream",  # 流式下载
    )


@router.post(
    path="/check-file-exists",
    response_model=Response[FileCheckResult],
)
async def check_file_exists(
        request: FileCheckRequest,
        file_service: FileService = Depends(get_file_service),
) -> Response[FileCheckResult]:
    """根据传递的路径判断文件是否存在"""
    result = await file_service.check_file_exists(file_path=request.file_path)

    return Response.success(
        msg="文件存在" if result.exists else "文件不存在",
        data=result,
    )


@router.post(
    path="/delete-file",
    response_model=Response[FileDeleteResult],
)
async def delete_file(
        request: FileDeleteRequest,
        file_service: FileService = Depends(get_file_service),
) -> Response[FileDeleteResult]:
    """根据传递的文件路径删除指定的文件"""
    result = await file_service.delete_file(
        file_path=request.file_path,
    )

    return Response.success(
        msg="删除文件成功",
        data=result,
    )
