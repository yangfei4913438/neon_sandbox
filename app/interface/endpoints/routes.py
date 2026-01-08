#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2025/12/12 21:13
@Author : YangFei
@File   : routes.py
@Desc   : 路由入口模块
"""
from fastapi import APIRouter
from . import file, shell, supervisor

def create_api_routes() -> APIRouter:
    """ 创建 API 路由 """
    # 创建路由实例对象
    api_router = APIRouter()

    # 添加模块路由
    api_router.include_router(file.router)
    api_router.include_router(shell.router)
    api_router.include_router(supervisor.router)

    # 返回路由实例
    return api_router


# 创建路由实例
router = create_api_routes()
