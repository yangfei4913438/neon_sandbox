#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2025/12/12 21:11
@Author : YangFei
@File   : shell.py
@Desc   : Shell模块路由
"""
import os.path

from fastapi import APIRouter, Depends

from app.interface.errors.exceptions import BadRequestException
from app.interface.schemas.base import Response
from app.interface.schemas.shell import ShellExecuteRequest, ShellReadRequest, ShellWriteRequest, ShellWaitRequest, \
    ShellKillRequest
from app.interface.service_dependencies import get_shell_service
from app.models.shell import ShellExecuteResult, ShellReadResult, ShellWaitResult, ShellWriteResult, ShellKillResult
from app.services.shell import ShellService

# Shell模块路由
router = APIRouter(prefix='/shell', tags=['Shell模块'])


@router.post(
    path='/exec-command',
    response_model=Response[ShellExecuteResult],
)
async def exec_command(
        request: ShellExecuteRequest,
        shell_service: ShellService = Depends(get_shell_service)
) -> Response[ShellExecuteResult]:
    """ 执行命令 """
    # 判断 session_id 是否存在，如果不存在则创建一个
    if not request.session_id or not request.session_id.strip():
        # 创建一个新的会话 ID
        request.session_id = shell_service.create_session_id(request.agent_id)

    # 判断是否传递了执行目录，如果没传递，则使用根目录作为执行目录
    if not request.exec_dir or not request.exec_dir.strip():
        # 使用当前用户的主目录作为执行目录
        request.exec_dir = os.path.expanduser('~')

    # 执行命令
    result = await shell_service.exec_command(
        session_id=request.session_id,
        exec_dir=request.exec_dir,
        command=request.command,
    )

    # 返回结果
    return Response.success(data=result)


@router.post(
    path='/read-shell-output',
    response_model=Response[ShellReadResult],
)
async def read_shell_output(
        request: ShellReadRequest,
        shell_service: ShellService = Depends(get_shell_service)
) -> Response[ShellReadResult]:
    """ 查看Shell会话 """
    # 判断 session_id 是否存在
    if not request.session_id or not request.session_id.strip():
        raise BadRequestException('session_id不能为空, 请核实后重试。')

    # 调用服务，获取命令执行结果
    result = await shell_service.read_shell_output(session_id=request.session_id, console=request.console)

    # 返回结果
    return Response.success(data=result)


@router.post(
    path='/wait-process',
    response_model=Response[ShellWaitResult],
)
async def wait_process(
        request: ShellWaitRequest,
        shell_service: ShellService = Depends(get_shell_service)
) -> Response[ShellWaitResult]:
    """ 等待Shell进程 """
    # 判断 session_id 是否存在
    if not request.session_id or not request.session_id.strip():
        raise BadRequestException('session_id不能为空, 请核实后重试。')

    # 调用服务，获取命令执行结果
    result = await shell_service.wait_process(session_id=request.session_id, seconds=request.seconds)

    # 返回结果
    return Response.success(
        msg=f"进程结束，返回状态码（returncode）: {result.returncode}",
        data=result
    )


@router.post(
    path='/write-shell-input',
    response_model=Response[ShellWriteResult],
)
async def write_shell_input(
        request: ShellWriteRequest,
        shell_service: ShellService = Depends(get_shell_service)
) -> Response[ShellWriteResult]:
    """ 写入数据到Shell子进程 """
    # 判断 session_id 是否存在
    if not request.session_id or not request.session_id.strip():
        raise BadRequestException('session_id不能为空, 请核实后重试。')

    # 调用服务，获取命令执行结果
    result = await shell_service.write_shell_input(
        session_id=request.session_id,
        input_text=request.input_text,
        press_enter=request.press_enter
    )

    # 返回结果
    return Response.success(msg="向子进程写入数据成功", data=result)


@router.post(
    path='/kill-process',
    response_model=Response[ShellKillResult]
)
async def kill_process(
        request: ShellKillRequest,
        shell_service: ShellService = Depends(get_shell_service)
) -> Response[ShellKillResult]:
    """ 写入数据到Shell子进程 """
    # 判断 session_id 是否存在
    if not request.session_id or not request.session_id.strip():
        raise BadRequestException('session_id不能为空, 请核实后重试。')

    # 调用服务，获取命令执行结果
    result = await shell_service.kill_process(session_id=request.session_id)

    # 返回结果
    return Response.success(
        msg="进程终止" if result.status == "terminated" else '进程已结束',
        data=result
    )
