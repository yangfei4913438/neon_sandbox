#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2025/12/12 21:34
@Author : YangFei
@File   : system_config.py
@Desc   : 系统配置
"""
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class SystemConfig(BaseSettings):
    """ 系统配置 """
    log_level: str = 'INFO'  # 日志级别
    server_timeout: int = 60  # 服务器超时时间，单位：分

    model_config = SettingsConfigDict(
        env_file='.env',  # 环境变量文件的路径
        env_file_encoding='utf-8',  # 环境变量文件的编码
        extra="ignore",  # 忽略传递进来的其他配置
    )


@lru_cache()
def get_settings() -> SystemConfig:
    """ 获取配置实例，使用 lru_cache 缓存以提高性能, 避免重复创建获取配置实例 """
    return SystemConfig()
