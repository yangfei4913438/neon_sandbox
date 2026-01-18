#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2026/1/17 14:47
@Author : YangFei
@File   : supervisor.py
@Desc   : 
"""
from typing import Optional

from pydantic import BaseModel, Field


class TimeoutRequest(BaseModel):
    """激活超时销毁请求"""
    minutes: Optional[int] = Field(default=None, description="分钟数")
