#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2025/12/12 21:17
@Author : YangFei
@File   : service_dependencies.py
@Desc   : 服务依赖注入
"""
from functools import lru_cache

from app.services.shell import ShellService
from app.services.file import FileService


@lru_cache()
def get_shell_service() -> ShellService:
    """ 获取 ShellService 实例 """
    return ShellService()


@lru_cache()
def get_file_service() -> FileService:
    """ 获取 FileService 实例 """
    return FileService()
