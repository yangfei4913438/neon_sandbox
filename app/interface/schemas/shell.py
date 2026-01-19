#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2025/12/12 23:16
@Author : YangFei
@File   : shell.py
@Desc   : shell 结构体定义
"""
from typing import Optional

from pydantic import BaseModel, Field


class ShellExecuteRequest(BaseModel):
    """ 执行命令请求结构体 """
    session_id: Optional[str] = Field(default=None, description='目标 Shell 会话的唯一标识符')
    exec_dir: Optional[str] = Field(default=None, description='执行命令的工作目录，必须是绝对路径')
    command: str = Field(..., description='要执行的 Shell 命令')


class ShellReadRequest(BaseModel):
    """ 查看Shell会话请求结构体 """
    session_id: str = Field(..., description='Shell 会话的唯一标识符')
    console: Optional[bool] = Field(default=None, description='是否返回控制台记录')


class ShellWaitRequest(BaseModel):
    """ 等待进程请求结构体 """
    session_id: str = Field(..., description='Shell 会话的唯一标识符')
    seconds: Optional[int] = Field(default=None, description='等待超时时间，单位为秒')


class ShellWriteRequest(BaseModel):
    """ 写入数据到子进程，请求结构体 """
    session_id: str = Field(..., description='Shell 会话的唯一标识符')
    input_text: str = Field(..., description='要写入子进程的文本数据')
    press_enter: bool = Field(default=True, description='是否在写入数据后按下回车键')


class ShellKillRequest(BaseModel):
    """ 杀死进程请求结构体 """
    session_id: str = Field(..., description='Shell 会话的唯一标识符')
