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


class FileReplaceRequest(BaseModel):
    """查找替换文件内容请求结构体"""
    file_path: str = Field(..., description="要替换内容的文件绝对路径")
    old_str: str = Field(..., description="要替换的原始字符串")
    new_str: str = Field(..., description="要替换的新字符串")
    sudo: Optional[bool] = Field(default=False, description="(可选)是否使用sudo权限")


class FileSearchRequest(BaseModel):
    """文件内容查找请求结构体"""
    file_path: str = Field(..., description="要查找内容的文件绝对路径")
    regex: str = Field(..., description="搜索正则表达式")
    sudo: Optional[bool] = Field(default=False, description="(可选)是否使用sudo权限")


class FileFindRequest(BaseModel):
    """文件查找请求结构体"""
    dir_path: str = Field(..., description="搜索的目录绝对路径")
    glob_pattern: str = Field(..., description="文件名模式(glob语法)")


class FileCheckRequest(BaseModel):
    """检查文件是否存在请求结构体"""
    file_path: str = Field(..., description="要检查是否存在的文件绝对路径")


class FileDeleteRequest(BaseModel):
    """删除文件请求结构体"""
    file_path: str = Field(..., description="要删除的文件绝对路径")
