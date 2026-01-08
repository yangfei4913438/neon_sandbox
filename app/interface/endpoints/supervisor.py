#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2025/12/12 21:12
@Author : YangFei
@File   : supervisor.py
@Desc   : supervisor模块路由
"""
from fastapi import APIRouter

# supervisor模块路由
router = APIRouter(prefix='/supervisors', tags=['supervisor模块'])

