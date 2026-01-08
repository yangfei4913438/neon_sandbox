#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2025/12/13 22:50
@Author : YangFei
@File   : file.py
@Desc   : 文件响应实体
"""
from typing import Optional
from pydantic import BaseModel, Field


class FileReadResult(BaseModel):
    """ 文件读取结果 """
    file_path: str = Field(..., description="文件路径")
    content: str = Field(..., description="文件内容")


class FileWriteResult(BaseModel):
    """文件写入结果"""
    file_path: str = Field(..., description="要写入的文件绝对路径")
    bytes_written: Optional[int] = Field(default=None, description="写入文件内容的字节数")
