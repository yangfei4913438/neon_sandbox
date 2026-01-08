#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2025/12/12 21:00
@Author : YangFei
@File   : main.py
@Desc   : 入口文件
"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.log_config import setup_logging
from app.core.system_config import get_settings
from app.interface.endpoints.routes import router
from app.interface.errors.exception_handles import register_exception_handlers

# 1. 获取配置实例(一定要基于 fastapi 项目运行，否则路径解析会出问题，例如找不到 core 模块)
settings = get_settings()

# 2. 初始化日志系统
setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """ 创建 FastAPI 应用的异步生命周期的上下文管理器 """
    # 启动时初始化资源
    logger.info("Neon Sandbox 正在初始化...")

    try:
        # yield 之前的代码在应用启动时执行
        yield  # 生命周期中间点

        # yield 之后的代码在应用关闭时执行
    finally:
        # 关闭时释放资源
        logger.info("Neon Sandbox 正在关闭...")


# 3. 定义 FastAPI 路由 tags 标签
tags_metadata = [
    {
        "name": "文件模块",
        "description": "包含 **文件增删改查** 等 API 接口。用于实现对沙箱文件的操作。",
    },
    {
        "name": "Shell模块",
        "description": "包含 **Shell命令执行** 等 API 接口。用于实现对沙箱 Shell 的操作。"
    },
    {
        "name": "Supervisor模块",
        "description": "使用接口+Supervisor 实现对沙箱系统中各种应用的管理。"
    }
]

# 4. 创建 FastAPI 应用实例
app = FastAPI(
    title="Neon Manus 沙箱系统",
    description="系统中预装了 Chrome、Python、Node.js, 支持运行 Shell 命令、文件管理等系统级操作。",
    version="1.0.0",
    openapi_tags=tags_metadata,
    lifespan=lifespan,  # 异步生命周期管理
)

# 5. 添加中间件
# 添加跨域中间件
app.add_middleware(
    # 可在此添加中间件，例如 CORS、请求日志等
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源访问
    allow_credentials=True,  # 允许携带凭证
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有请求头
)

# 6. 注册全局异常处理器
register_exception_handlers(app=app)

# 7. 导入并注册路由
app.include_router(router=router, prefix="/api")
