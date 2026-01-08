#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2025/12/13 22:52
@Author : YangFei
@File   : file.py
@Desc   : file 结构体定义
"""
from typing import Optional

from pydantic import BaseModel, Field


class FileReadRequest(BaseModel):
    """ 读取文件请求 """
    file_path: str = Field(..., description="文件绝对路径")
    start_line: int = Field(default=0, description="可选，读取的起始行，索引从 0 开始。")
    end_line: Optional[int] = Field(default=None, description="可选，结束行号，返回内容不包含该行")
    sudo: bool = Field(default=False, description="是否使用 sudo 权限读取文件")
    max_length: int = Field(default=10000, description="可选，最大返回长度，默认 10000 字符")


class FileWriteRequest(BaseModel):
    """ 写入文件请求 """
    file_path: str = Field(..., description="文件绝对路径")
    content: str = Field(..., description="要写入的文件内容")
    append: bool = Field(default=False, description="可选，是否追加写入，默认覆盖写入")
    leading_newline: bool = Field(default=False, description="可选，是否在写入内容前，添加换行符")
    trailing_newline: bool = Field(default=False, description="可选，是否在写入内容结尾，添加换行符")
    sudo: bool = Field(default=False, description="可选，是否使用 sudo 权限写入文件")
