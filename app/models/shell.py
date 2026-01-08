#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2025/12/12 23:31
@Author : YangFei
@File   : shell.py
@Desc   : shell 响应实体
"""
import asyncio.subprocess
from typing import Optional, List

from pydantic import BaseModel, Field, ConfigDict


class ConsoleRecord(BaseModel):
    """ Shell命令控制台记录 """
    ps1: str = Field(..., description="命令提示符")
    command: str = Field(..., description="Shell命令")
    output: str = Field(..., description="Shell命令输出")


class Shell(BaseModel):
    """ Shell 会话模型"""
    process: asyncio.subprocess.Process = Field(..., description="会话中的子进程")
    exec_dir: str = Field(..., description="会话执行目录")
    output: str = Field(..., description="会话输出")
    console_records: List[ConsoleRecord] = Field(default_factory=list, description="会话控制台记录列表")

    # 因为有非默认类型，所以这里要允许扩展
    model_config = ConfigDict(
        arbitrary_types_allowed=True,  # 允许任意类型
    )


class ShellWaitResult(BaseModel):
    """ shell 等待结果 """
    returncode: int = Field(..., description="子进程返回代码")


class ShellReadResult(BaseModel):
    """ shell 查看结果 """
    session_id: str = Field(..., description="Shell 会话 ID")
    output: str = Field(default=None, description="Shell 会话的输出内容")
    console_records: List[ConsoleRecord] = Field(default_factory=list, description="Shell 会话的控制台记录列表")


class ShellExecuteResult(BaseModel):
    """ shell 执行结果 """
    session_id: str = Field(..., description="Shell 会话 ID")
    command: str = Field(..., description="执行的命令")
    status: str = Field(..., description="命令执行状态")
    returncode: Optional[int] = Field(default=None, description="执行返回代码，只有执行完成后才有值")
    output: Optional[str] = Field(default=None, description="命令执行输出，只有执行完成后才有值")


class ShellWriteResult(BaseModel):
    """ shell 写入结果 """
    status: str = Field(..., description="写入状态")


class ShellKillResult(BaseModel):
    """ shell 终止结果 """
    status: str = Field(..., description="进程状态")
    returncode: int = Field(..., description="进程返回代码")
