#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2025/12/12 22:27
@Author : YangFei
@File   : exceptions.py
@Desc   : 定义异常对象
"""
import logging
from typing import Any

from fastapi import status

logger = logging.getLogger(__name__)


class AppException(Exception):
    """ 应用基础异常 """

    def __init__(
            self,
            msg: str = '应用发送错误，请稍后再试',
            status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
            data: Any = None
    ) -> None:
        """ 异常消息初始化 """
        self.status_code = status_code
        self.msg = msg
        self.data = data

        logger.error(f'沙箱异常: {msg}, 错误码: {status_code}, 数据: {data}')

        # 执行父类构造函数
        super().__init__(self.msg)


class NotFoundException(AppException):
    """ 资源未找到异常类，继承自 AppException """

    def __init__(self, msg: str = '资源未找到, 请检查后重试.') -> None:
        super().__init__(msg=msg, status_code=status.HTTP_404_NOT_FOUND)


class BadRequestException(AppException):
    """ 客户端请求异常类，继承自 AppException """

    def __init__(self, msg: str = '客户端请求错误，请检查后重试.') -> None:
        super().__init__(msg=msg, status_code=status.HTTP_400_BAD_REQUEST)
